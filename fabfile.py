import os
import logging

from fabric.api import (
    abort,
    cd,
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
    with settings(warn_only=True):
        with cd(LOCAL_BACKEND_DIR):
            logger.info("Running local tests.")
            result = local('tox', capture=True)
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


def setup_nginx():
    copy_nginx_config()
    restart_nginx()


def deploy():
    # run_tests()
    launch_docker()
    create_directories()
    checkout_repository()
    stop_previous_containers()
    fix_premissions()
    prepare_frontend()
    launch_containers()
    set_secret_key()
    setup_nginx()
    restart_nginx()
