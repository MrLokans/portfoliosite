import os
import time
import logging

from fabric.api import abort, cd, get, local, put, run, settings, sudo
from fabric.context_managers import hide
from fabric.contrib.files import upload_template
from fabric.state import env

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fabric")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOCAL_CONFIG_DIR = os.path.join(BASE_DIR, "deployment")

SECRET_KEY_FILE = os.path.abspath("secret.key")
REPOSITORY_URL = "https://github.com/MrLokans/portfoliosite"
DEPLOYMENT_DIR = "/opt/mrlokans.com"
REMOTE_BACKEND_DIR = os.path.join(DEPLOYMENT_DIR, "backend")
REMOTE_STATIC_DIR = os.path.join(DEPLOYMENT_DIR, "static")
NGINX_CONFIG_NAME = "mrlokans.com.conf"
NGINX_CONFIG_LOCAL_PATH = os.path.abspath(
    os.path.join(LOCAL_CONFIG_DIR, "nginx", NGINX_CONFIG_NAME)
)
NGINX_CONFIG_REMOTE_PATH = os.path.join("/etc/nginx/sites-available", NGINX_CONFIG_NAME)
NGINX_SYMLINK_REMOTE_PATH = os.path.join("/etc/nginx/sites-enabled", NGINX_CONFIG_NAME)
SYSTEMD_UNIT_NAME = "personalsite-backend.service"

SYSTEMD_UNIT_LOCAL_PATH = os.path.join(LOCAL_CONFIG_DIR, SYSTEMD_UNIT_NAME)
SYSTEMD_UNIT_REMOTE_PATH = os.path.join("/etc/systemd/system/", SYSTEMD_UNIT_NAME)
ENV_VARS_FILE = ".env"
REGISTRY_URL = "registry.mrlokans.com:5000"


DISABLED_MAINTENANCE_PAGE = os.path.join(
    DEPLOYMENT_DIR, "deployment", "nginx", "maintenance_off.html"
)
ENABLED_MAINTENANCE_PAGE_NAME = os.path.join(
    DEPLOYMENT_DIR, "deployment", "nginx", "maintenance_on.html"
)

REGISTRY_CERTS_DIR = "/etc/letsencrypt/live/registry.mrlokans.com"

# Health check settings
HEALTHCHECK_URL = "https://mrlokans.com/api/health/"
AWAIT_TIMEOUT_IN_SEC, PAUSE_TIMEOUT = 60, 5


env.hosts = ["mrlokans@188.166.109.166"]
env.revision = getattr(env, "revision", "develop")
env.backend_container_version = getattr(env, "backend_container_version", "latest")


def _get_backend_container_id():
    with settings(hide("running", "commands", "stdout")):
        output = sudo("docker ps | grep backend | awk '{print $1}'", warn_only=True)
        return output


def _exec_docker_command(container_id: str, command: str) -> str:
    exec_command = "docker exec -it {id} {command}".format(
        id=container_id, command=command
    )
    return sudo(exec_command)


def create_directories():
    sudo("mkdir -p {}".format(DEPLOYMENT_DIR))
    sudo("chown -R {user}:{user} {dir}".format(user=env.user, dir=DEPLOYMENT_DIR))


def copy_configuration_files():
    files_to_copy = (
        'docker-compose.prod.yml',
        'deployment/nginx/maintenance_off.html',
        'deployment/manage.sh',
    )
    with cd(DEPLOYMENT_DIR):
        for filename in files_to_copy:
            put(filename, filename, use_sudo=True)
        sudo(f"chmod +x deployment/manage.sh")


def launch_docker():
    with settings(warn_only=True):
        logger.info("Checking docker daemon is running.")
        result = sudo("docker ps")
        if not result.failed:
            return
        logger.info("Docker is not running. " "Attempting to launch.")
        result = sudo("systemctl start docker")
        if result.failed:
            abort("Docker is not installed on the host.")


def run_tests():
    logger.info("Running local tests.")
    result = local("tox")
    if result.failed:
        abort("Tests failed.")


def stop_previous_containers():
    with cd(DEPLOYMENT_DIR):
        logger.info("Stopping any previously " "running containers.")
        sudo("docker-compose -f docker-compose.prod.yml stop")


def launch_containers():
    with cd(DEPLOYMENT_DIR):
        logger.info("Launching backend container")
        sudo("docker-compose -f docker-compose.prod.yml up --build -d backend")


def copy_local_environment_settings():
    """
    Copies local environment settings files
    """
    put(".deployment-env", os.path.join(DEPLOYMENT_DIR, ENV_VARS_FILE))


def copy_nginx_config():
    logger.info("Copying nginx config.")
    put(NGINX_CONFIG_LOCAL_PATH, NGINX_CONFIG_REMOTE_PATH, use_sudo=True)
    with settings(warn_only=True):
        logger.info("Activating the nginx config.")
        sudo(
            "ln -s {available} {enabled}".format(
                available=NGINX_CONFIG_REMOTE_PATH, enabled=NGINX_SYMLINK_REMOTE_PATH
            )
        )


def restart_nginx():
    logger.info("Restarting nginx.")
    sudo("systemctl restart nginx")


def backup_database():
    """
    Dumps active database, archives it,
    and downloads for local usage
    """

    def generate_backup_name():
        date = time.strftime("%Y-%m-%d_%H-%M-%S")
        name = "database-backup-{}.tar.gz".format(date)
        return name

    local("mkdir -p backups")
    backup_name = generate_backup_name()
    with cd(os.path.join(DEPLOYMENT_DIR)), settings(warn_only=True):
        sudo(
            "tar -zcvf {archive} {postgres_dir}".format(
                archive=backup_name, postgres_dir="backend/mydatabase"
            )
        )
        get(remote_path=backup_name, local_path=os.path.join("backups", backup_name))


def setup_nginx():
    copy_nginx_config()
    restart_nginx()


def setup_seo():
    """
    Copies robots.txt and sitemap.xml files
    to nginx root
    """
    logger.info("Copying robots.txt and sitemap.xml")
    put("robots.txt", REMOTE_STATIC_DIR, use_sudo=True)
    put("sitemap.xml", REMOTE_STATIC_DIR, use_sudo=True)


def pull_backend_image():
    # Check credentials in environment
    if "DOCKER_USERNAME" not in env and "DOCKER_PASSWORD" not in env:
        raise ValueError('"DOCKER_USERNAME" or "DOCKER_PASSWORD" env var is missing.')
    login_cmd = "docker login -u {login} -p {password} {registry}"
    with hide("output"):
        sudo(
            login_cmd.format(
                login=env.DOCKER_USERNAME,
                password=env.DOCKER_PASSWORD,
                registry=REGISTRY_URL,
            )
        )
    pull_cmd = "docker pull {registry}/{image}:{version}"
    sudo(
        pull_cmd.format(
            registry=REGISTRY_URL,
            image="personal_site",
            version=env.backend_container_version,
        )
    )


def copy_systemd_unit():
    """
    Copy service file to the
    remote directory
    """
    logger.info("Copying systemd service file.")
    put(SYSTEMD_UNIT_LOCAL_PATH, SYSTEMD_UNIT_REMOTE_PATH, use_sudo=True)


def enable_systemd_unit():
    """
    Mark unit as enabled to
    make sure container is started at the reboot
    time
    """
    logger.info("Enabling systemd unit.")
    sudo("systemctl enable {unit}".format(unit=SYSTEMD_UNIT_NAME))


def enable_maintenance_page():
    """
    Tell nginx that site is unavailable and show
    the maintenance page.

    Check the nginx config for details.
    """
    sudo("mv {} {}".format(DISABLED_MAINTENANCE_PAGE, ENABLED_MAINTENANCE_PAGE_NAME))


def disable_maintenance_page():
    """
    Tell nginx that site is unavailable and show
    the maintenance page.

    Check the nginx config for details.
    """
    with settings(warn_only=True):
        sudo(
            "mv {} {}".format(ENABLED_MAINTENANCE_PAGE_NAME, DISABLED_MAINTENANCE_PAGE)
        )


def setup_autostart():
    copy_systemd_unit()
    enable_systemd_unit()


def check_site_availability():
    time_already_waiting = 0
    started = time.monotonic()
    while time_already_waiting < AWAIT_TIMEOUT_IN_SEC:
        response = requests.get(HEALTHCHECK_URL, headers={"Accept": "application/json"})
        if response.status_code == 200:
            logger.info("Site is available!")
            return
        logger.info("Could not reach the site, waiting for %s seconds", PAUSE_TIMEOUT)
        time.sleep(PAUSE_TIMEOUT)
        time_already_waiting = time.monotonic() - started
    logger.error(
        "Waiting more than %s seconds, back-end does not work!", AWAIT_TIMEOUT_IN_SEC
    )
    enable_maintenance_page()


def renew_certificates():
    sudo("systemctl stop nginx")
    sudo("certbot renew")
    with cd(REGISTRY_CERTS_DIR):
        sudo("cp privkey.pem domain.key")
        sudo("cat cert.pem chain.pem > domain.crt")
    sudo("systemctl start nginx")


def manage():
    """
    Runs remote django management command
    """
    command = input("Enter the management command > ")  # nosec
    container_id = _get_backend_container_id()
    _exec_docker_command(container_id, command)
def setup_periodic_jobs():
    """
    Creates application specific crontab file
    on the target server and registers it within
    the crontab scheduler to periodicaly run required
    jobs
    """
    target_crontab_dir = "/etc/cron.d/mrlokans.com"
    upload_template(
        filename="deployment/crontab.template",
        destination=target_crontab_dir,
        context={
            'APPLICATION_DIR': DEPLOYMENT_DIR,
            'MANAGEMENT_SCRIPT_PATH': './deployment/manage.sh',
            'LOG_DIR': '/var/log/cron',
        },
        use_sudo=True, backup=False,
    )
    upload_template(
        filename="deployment/logrotate.template",
        destination="/etc/logrotate.d/mrlokanslogs",
        context={
            'LOG_DIR': '/var/log/cron',
        },
        use_sudo=True, backup=False,
    )
    sudo(f"crontab {target_crontab_dir}")


def deploy():
    launch_docker()
    create_directories()
    backup_database()
    copy_configuration_files()
    pull_backend_image()
    copy_local_environment_settings()
    maintenance_started = time.monotonic()
    enable_maintenance_page()
    stop_previous_containers()
    launch_containers()
    setup_nginx()
    setup_seo()
    disable_maintenance_page()
    restart_nginx()
    maintenance_finished = time.monotonic()
    logger.info(
        "Site was unavailable for %d seconds",
        maintenance_finished - maintenance_started,
    )
    setup_autostart()
    check_site_availability()
