import os
import logging

from fabric.api import (
    abort,
    cd,
    local,
    lcd,
    run,
    settings,
    sudo
)
from fabric.state import env

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fabric")

LOCAL_BACKEND_DIR = os.path.abspath('backend')
LOCAL_FRONTEND_DIR = os.path.abspath('frontend')
REPOSITORY_URL = 'https://github.com/MrLokans/portfoliosite'
REPOSITORY_PATH = '/opt/personalsite'
REMOTE_BACKEND_DIR = os.path.join(REPOSITORY_PATH, 'backend')
REMOTE_FRONTEND_DIR = os.path.join(REPOSITORY_PATH, 'frontend')

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
                run('git checkout')
                run('git pull')


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
    with cd(REMOTE_BACKEND_DIR):
        logger.info("Stopping any previously "
                    "running containers.")
        sudo('docker-compose stop')


def launch_containers():
    with cd(REMOTE_BACKEND_DIR):
        logger.info("Building new containers")
        sudo('docker-compose build')
        logger.info('Launching new containers')
        sudo('docker-compose up -d')


def restart_nginx():
    sudo('systemctl restart nginx')


def deploy():
    # run_tests()
    launch_docker()
    create_directories()
    checkout_repository()
    stop_previous_containers()
    launch_containers()
    restart_nginx()
