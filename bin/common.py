#!/usr/bin/env python3
import configparser
import logging
from logging.handlers import RotatingFileHandler
import os


# some constants
PROG_NAME = 'metachine'
MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
APPS_DIR = os.path.join(MAIN_DIR, 'apps')
CONF_DIR = os.path.join(MAIN_DIR, 'conf')
LOGS_DIR = os.path.join(MAIN_DIR, 'logs')
VENV_DIR = os.path.join(MAIN_DIR, 'venv')
VENV_PIP = os.path.join(VENV_DIR, 'bin', 'pip')
VENV_PY = os.path.join(VENV_DIR, 'bin', 'python')


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
LOG = create_logger()


def get_config():
    LOG.info("Reading configuration")
    settings = {}
    config = configparser.ConfigParser()
    config.read(os.path.join(CONF_DIR, PROG_NAME + '.conf'))
    return config
CONFIG = get_config()
