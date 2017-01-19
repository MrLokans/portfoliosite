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

BACKEND_DIR = os.path.abspath('backend')
FRONTEND_DIR = os.path.abspath('fronted')
REPOSITORY_URL = 'https://github.com/MrLokans/portfoliosite'
REPOSITORY_PATH = '/opt/personalsite'

env.hosts = []

is_local = not env.hosts
if is_local:
    run = local
    cd = lcd


def create_directories():
    sudo('mkdir -p {}'.format(REPOSITORY_PATH))
    sudo('chown -R {user}:{user} {dir}'.format(user=env.user,
                                               dir=REPOSITORY_PATH))


def launch_docker():
    with settings(warn_only=True):
        logger.info("Checking docker daemon is running.")
        result = run('docker ps', capture=True)
        if not result.failed:
            return
        logger.info("Docker is not running. "
                    "Attempting to launch.")
        result = run('sudo systemctl start docker', capture=True)
        if result.failed:
            abort("Docker is not installed on the host.")


def run_tests():
    with settings(warn_only=True):
        with cd(BACKEND_DIR):
            logger.info("Running local tests.")
            result = run('tox', capture=True)
            if result.failed:
                abort("Tests failed.")


def stop_previous_containers():
    logger.info("Stopping any previously "
                "running containers.")
    run('docker-compose stop')


def launch_containers():
    logger.info("Launching new containers")
    run('docker-compose up --build -d')


def deploy():
    run_tests()
    launch_docker()
    create_directories()
    stop_previous_containers()
    launch_containers()
