#!/usr/bin/env python3
#    import ipdb;ipdb.set_trace()
import logging
from logging.handlers import RotatingFileHandler
import os
import subprocess
import sys
# local
from common import *


def clean():
    print("You will erase all installed applications, NOT your associated data.")
    sure = input("Are you sure? [y/N] ")
    if (sure == 'y'):
        for directory in os.listdir(APPS_DIR):
            app_directory = os.path.join(APPS_DIR, directory)
            if os.path.isdir(app_directory):
                LOG.info("Erasing " + directory)
                subprocess.call(['rm', '-rf', app_directory])

        if os.path.isdir(VENV_DIR):
            subprocess.call(['rm', '-rf', VENV_DIR])
            LOG.info("Erasing virtual environment")


if __name__ == '__main__':
    clean()
