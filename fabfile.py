import os
import time
import logging

from fabric.api import (
    abort, cd, get, local, lcd,
    put, run, settings, sudo
)
from fabric.context_managers import hide
from fabric.state import env

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fabric")

SECRET_KEY_FILE = os.path.abspath('secret.key')
LOCAL_BACKEND_DIR = os.path.abspath('backend')
REPOSITORY_URL = 'https://github.com/MrLokans/portfoliosite'
DEPLOYMENT_DIR = '/opt/mrlokans.com'
REMOTE_BACKEND_DIR = os.path.join(DEPLOYMENT_DIR, 'backend')
REMOTE_STATIC_DIR = os.path.join(DEPLOYMENT_DIR, 'static')
NGINX_CONFIG_NAME = 'mrlokans.com.conf'
NGINX_CONFIG_LOCAL_PATH = os.path.abspath(os.path.join('nginx',
                                                       NGINX_CONFIG_NAME))
NGINX_CONFIG_REMOTE_PATH = os.path.join('/etc/nginx/sites-available',
                                        NGINX_CONFIG_NAME)
NGINX_SYMLINK_REMOTE_PATH = os.path.join('/etc/nginx/sites-enabled',
                                         NGINX_CONFIG_NAME)
SYSTEMD_UNIT_NAME = 'personalsite-backend.service'
SYSTEMD_UNIT_LOCAL_PATH = os.path.abspath(SYSTEMD_UNIT_NAME)
SYSTEMD_UNIT_REMOTE_PATH = os.path.join('/etc/systemd/system/',
                                        SYSTEMD_UNIT_NAME)
CRONTAB_LOCAL_PATH = os.path.join(LOCAL_BACKEND_DIR, 'crontab')
ENV_VARS_FILE = '.env'


DISABLED_MAINTENANCE_PAGE = os.path.join(
    DEPLOYMENT_DIR, 'nginx', 'maintenance_off.html'
)
ENABLED_MAINTENANCE_PAGE_NAME = os.path.join(
    DEPLOYMENT_DIR, 'nginx', 'maintenance_on.html'
)


env.hosts = ['mrlokans@mrlokans.com']
env.revision = getattr(env, 'revision', 'develop')


def _get_backend_container_id():
    with settings(hide('running', 'commands', 'stdout')):
        output = sudo("docker ps | grep backend | awk '{print $1}'", warn_only=True)
        return output


def _exec_docker_command(container_id: str, command: str) -> str:
    exec_command = "docker exec -it {id} {command}".format(id=container_id, command=command)
    return sudo(exec_command)


def create_directories():
    sudo('mkdir -p {}'.format(DEPLOYMENT_DIR))
    sudo('chown -R {user}:{user} {dir}'.format(user=env.user,
                                               dir=DEPLOYMENT_DIR))


def checkout_repository():
    with cd(DEPLOYMENT_DIR):
        with settings(warn_only=True):
            result = run('git clone {url} {path}'.format(url=REPOSITORY_URL,
                                                         path=DEPLOYMENT_DIR))
            if result.failed:
                logger.info("Repository is already cloned. "
                            "Checkout will be attempted "
                            "together with pulling.")
                run('git reset --hard HEAD')
            run('git fetch --all')
            run('git checkout %s' % env.revision)
            run('git pull')


def fix_premissions():
    with cd(REMOTE_BACKEND_DIR):
        sudo('chmod +x entrypoint.sh')


def launch_docker():
    with settings(warn_only=True):
        logger.info("Checking docker daemon is running.")
        result = sudo('docker ps')
        if not result.failed:
            return
        logger.info("Docker is not running. "
                    "Attempting to launch.")
        result = sudo('systemctl start docker')
        if result.failed:
            abort("Docker is not installed on the host.")


def run_tests():
    with lcd(LOCAL_BACKEND_DIR):
        logger.info("Running local tests.")
        result = local('tox')
        if result.failed:
            abort("Tests failed.")


def stop_previous_containers():
    with cd(DEPLOYMENT_DIR):
        logger.info("Stopping any previously "
                    "running containers.")
        sudo('docker-compose -f docker-compose.prod.yml stop')


def build_containers():
    with cd(DEPLOYMENT_DIR):
        logger.info("Building new containers")
        sudo('docker-compose -f docker-compose.prod.yml build')


def launch_containers():
    with cd(DEPLOYMENT_DIR):
        logger.info('Launching backend container')
        sudo('docker-compose -f docker-compose.prod.yml up -d backend')


def set_secret_key():
    """
    It is strongly recommended to use
    environment variables instead.
    """
    logger.info("Reading secret key.")
    with open(SECRET_KEY_FILE, 'r') as f:
        secret_key = f.read()
    assert secret_key

    logger.info("Writing new secret key.")
    sudo('sed -i \'s/.*SECRET_KEY.*/SECRET_KEY="{key}"/\' {path}/backend/personal_site/settings/prod.py'
         .format(key=secret_key, path=DEPLOYMENT_DIR))


def copy_local_environment_settings():
    """
    Copies local environment settings files
    """
    put('.deployment-env', os.path.join(DEPLOYMENT_DIR, ENV_VARS_FILE))


def copy_nginx_config():
    logger.info("Copying nginx config.")
    put(NGINX_CONFIG_LOCAL_PATH, NGINX_CONFIG_REMOTE_PATH,
        use_sudo=True)
    with settings(warn_only=True):
        logger.info('Activating the nginx config.')
        sudo('ln -s {available} {enabled}'.
             format(available=NGINX_CONFIG_REMOTE_PATH,
                    enabled=NGINX_SYMLINK_REMOTE_PATH))


def restart_nginx():
    logger.info("Restarting nginx.")
    sudo('systemctl restart nginx')


def backup_database():
    """
    Dumps active database, archives it,
    and downloads for local usage
    """

    def generate_backup_name():
        date = time.strftime('%Y-%m-%d_%H-%M-%S')
        name = "database-backup-{}.tar.gz".format(date)
        return name

    local('mkdir -p backups')
    backup_name = generate_backup_name()
    with cd(os.path.join(DEPLOYMENT_DIR)), settings(warn_only=True):
        sudo('tar -zcvf {archive} {postgres_dir}'
             .format(archive=backup_name,
                     postgres_dir='backend/mydatabase',
                     ))
        get(remote_path=backup_name,
            local_path=os.path.join('backups', backup_name))


def setup_nginx():
    copy_nginx_config()
    restart_nginx()


def setup_seo():
    '''
    Copies robots.txt and sitemap.xml files
    to nginx root
    '''
    logger.info("Copying robots.txt and sitemap.xml")
    put('robots.txt', REMOTE_STATIC_DIR,
        use_sudo=True)
    put('sitemap.xml', REMOTE_STATIC_DIR,
        use_sudo=True)


def copy_systemd_unit():
    """
    Copy service file to the
    remote directory
    """
    logger.info("Copying systemd service file.")
    put(SYSTEMD_UNIT_LOCAL_PATH, SYSTEMD_UNIT_REMOTE_PATH,
        use_sudo=True)


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
    sudo('mv {} {}'.format(DISABLED_MAINTENANCE_PAGE, ENABLED_MAINTENANCE_PAGE_NAME))


def disable_maintenance_page():
    """
    Tell nginx that site is unavailable and show
    the maintenance page.

    Check the nginx config for details.
    """
    with settings(warn_only=True):
        sudo('mv {} {}'.format(ENABLED_MAINTENANCE_PAGE_NAME, DISABLED_MAINTENANCE_PAGE))


def setup_autostart():
    copy_systemd_unit()
    enable_systemd_unit()


def manage():
    """
    Runs remote django management command
    """
    command = input("Enter the management command > ")
    container_id = _get_backend_container_id()
    _exec_docker_command(container_id, command)


def deploy():
    run_tests()
    backup_database()
    launch_docker()
    create_directories()
    backup_database()
    checkout_repository()
    copy_local_environment_settings()
    fix_premissions()
    set_secret_key()
    build_containers()
    maintenance_started = time.monotonic()
    enable_maintenance_page()
    stop_previous_containers()
    launch_containers()
    setup_nginx()
    setup_seo()
    disable_maintenance_page()
    restart_nginx()
    maintenance_finished = time.monotonic()
    logger.info('Site was unavailable for %d seconds', maintenance_finished - maintenance_started)
    setup_autostart()
