import os
import logging

from fabric.api import (
    abort,
    cd,
    local,
    lcd,
    run,
    settings
)
from fabric.state import env

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fabric")

BACKEND_DIR = os.path.abspath('backend')
FRONTEND_DIR = os.path.abspath('fronted')

is_local = not env.hosts
if is_local:
    run = local
    cd = lcd


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


def deploy():
    launch_docker()
    run_tests()
