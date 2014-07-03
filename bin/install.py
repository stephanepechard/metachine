#!/usr/bin/env python3
#    import ipdb;ipdb.set_trace()
# system
import os
import subprocess
import sys
# local
from common import *


def make_venv():
    if not os.path.exists(VENV_DIR):
        try:
            LOG.info("No virtual environment available, create one")
            subprocess.call(['pyvenv', VENV_DIR])
            LOG.info("Virtual environment created in " + VENV_DIR)
        except FileNotFoundError:
            LOG.error("pyvenv not found, please install and use Python >= 3.3")
            sys.exit(1)
    else:
        LOG.info("Virtual environment found, checking it...")

    # install stuff in it
    packages = [app.strip() for app in CONFIG['DEFAULT']['packages'].split(',')]
    subprocess.call([VENV_PIP, '-q', 'install'] + packages)


def install_apps():
    for app in [app.strip() for app in CONFIG['apps']['list'].split(',')]:
        app_dir = os.path.join(APPS_DIR, app)
        if app in CONFIG.sections() and 'type' in CONFIG[app]:
            LOG.info("Installing " + app)
            if 'git' in CONFIG[app]['type'] and 'url' in CONFIG[app] and 'tag' in CONFIG[app]:
                subprocess.call(['git', 'clone', CONFIG[app]['url'], app_dir, '-q'])
                subprocess.call(['cd', app_dir, '&&', 'git', 'checkout', CONFIG[app]['tag'], '-q'])


def install():
    os.chdir(MAIN_DIR)

    make_venv()
    install_apps()

    # plug conf, data, logs, media, etc.
    # create links with supervisord, nginx, etc.


if __name__ == '__main__':
    install()
