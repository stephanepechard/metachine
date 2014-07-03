#!/usr/bin/env python3
#    import ipdb;ipdb.set_trace()
import configparser
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import subprocess
import sys


# some constants
PROG_NAME = 'metachine'
MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
APPS_DIR = os.path.join(MAIN_DIR, 'apps')
CONF_DIR = os.path.join(MAIN_DIR, 'conf')
LOGS_DIR = os.path.join(MAIN_DIR, 'logs')
VENV_DIR = os.path.join(MAIN_DIR, 'venv')


def create_logger():
    logger = logging.getLogger(PROG_NAME)
    logger.setLevel(logging.DEBUG) 
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

    # file handler
    file_handler = RotatingFileHandler(os.path.join(LOGS_DIR, PROG_NAME + '.log'), 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
 
    # console handler
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    logger.addHandler(steam_handler) 
    return logger
log = create_logger()


def get_config():
    log.info("Reading configuration")
    settings = {}
    config = configparser.ConfigParser()
    config.read(os.path.join(CONF_DIR, PROG_NAME + '.conf'))

#    settings['apps'] = [app.strip() for app in config['apps']['list'].split(',')]
    return config


def make_venv():
    # create it
    if not os.path.exists(VENV_DIR):
        try:
            log.info("No virtual environment available, create one")
            subprocess.call(['pyvenv', VENV_DIR])
            log.info("Virtual environment created in " + VENV_DIR)
        except FileNotFoundError:
            log.error("pyvenv not found, please install and use Python >= 3.3")
            sys.exit(1)
    else:
        log.info("Virtual environment found, checking it...")


def install_apps(config):
    for app in [app.strip() for app in config['apps']['list'].split(',')]:
        app_dir = os.path.join(APPS_DIR, app)
        if app in config.sections() and 'type' in config[app]:
            log.info("Installing " + app)
            if 'git' in config[app]['type'] and 'url' in config[app] and 'tag' in config[app]:
                subprocess.call(['git', 'clone', config[app]['url'], app_dir])
                subprocess.call(['cd', app_dir, '&&', 'git', 'checkout', config[app]['tag']])


def main():
    os.chdir(MAIN_DIR)
    make_venv()
    config = get_config()

    install_apps(config)

    # get external apps
    # log.info("Install external applications...")

    # plug conf, data, logs, media, etc.
    # create links with supervisord, nginx, etc.


if __name__ == '__main__':
    main()
