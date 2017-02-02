import os
import time
import logging

from fabric.api import (
    abort,
    cd,
    get,
    local,
    lcd,
    put,
    run,
    settings,
    sudo
)
from fabric.state import env

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fabric")

SECRET_KEY_FILE = os.path.abspath('secret.key')
LOCAL_BACKEND_DIR = os.path.abspath('backend')
LOCAL_FRONTEND_DIR = os.path.abspath('frontend')
REPOSITORY_URL = 'https://github.com/MrLokans/portfoliosite'
REPOSITORY_PATH = '/opt/personalsite'
REMOTE_BACKEND_DIR = os.path.join(REPOSITORY_PATH, 'backend')
REMOTE_FRONTEND_DIR = os.path.join(REPOSITORY_PATH, 'frontend')
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

env.hosts = []


def create_directories():
    sudo('mkdir -p {}'.format(REPOSITORY_PATH))
    sudo('chown -R {user}:{user} {dir}'.format(user=env.user,
                                               dir=REPOSITORY_PATH))


def checkout_repository():
    with cd(REPOSITORY_PATH):
        with settings(warn_only=True):
            result = run('git clone {url} {path}'.format(url=REPOSITORY_URL,
                                                         path=REPOSITORY_PATH))
            if result.failed:
                logger.info("Repository is already cloned. "
                            "Checkout will be attempted "
                            "together with pulling.")
                run('git reset --hard HEAD')
                run('git pull')


def fix_premissions():
    with cd(REMOTE_BACKEND_DIR):
        sudo('chmod +x entrypoint.sh')
        sudo('chmod +x entrypoint-prod.sh')
    with cd(REMOTE_FRONTEND_DIR):
        sudo('chmod +x entrypoint-prod.sh')


def prepare_frontend():
    with cd(REMOTE_FRONTEND_DIR):
        run('npm install')
        run('npm install gulp')
        run('bower install')


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
    with cd(REPOSITORY_PATH):
        logger.info("Stopping any previously "
                    "running containers.")
        sudo('docker-compose -f docker-compose.prod.yml stop')


def launch_containers():
    with cd(REPOSITORY_PATH):
        logger.info("Building new containers")
        sudo('docker-compose -f docker-compose.prod.yml build')
        logger.info("Building front-end")
        sudo('docker-compose -f docker-compose.prod.yml up  frontend')
        logger.info('Launching backend container')
        sudo('docker-compose -f docker-compose.prod.yml up -d backend')


def set_secret_key():
    """
    It is strongly recommended to use
    environment variables instead.
    """
    secret_key = ""
    logger.info("Reading secret key.")
    with open(SECRET_KEY_FILE, 'r') as f:
        secret_key = f.read()
    assert secret_key

    logger.info("Writing new secret key.")
    sudo('sed -i \'s/.*SECRET_KEY.*/SECRET_KEY="{key}"/\' {path}/backend/personal_site/settings/prod.py'
         .format(key=secret_key, path=REPOSITORY_PATH))


def copy_nginx_config():
    logger.info("Copying nginx config.")
    put(NGINX_CONFIG_LOCAL_PATH, NGINX_CONFIG_REMOTE_PATH,
        use_sudo=True)
    with settings(warn_only=True):
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
    with cd(REPOSITORY_PATH), settings(warn_only=True):
        sudo('ls -la')
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
    put('robots.txt', '/opt/personalsite/frontend/build',
        use_sudo=True)
    put('sitemap.xml', '/opt/personalsite/frontend/build',
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


def setup_autostart():
    copy_systemd_unit()
    enable_systemd_unit()


def deploy():
    run_tests()
    backup_database()
    launch_docker()
    create_directories()
    checkout_repository()
    stop_previous_containers()
    fix_premissions()
    prepare_frontend()
    set_secret_key()
    launch_containers()
    setup_nginx()
    setup_seo()
    restart_nginx()
    setup_autostart()
