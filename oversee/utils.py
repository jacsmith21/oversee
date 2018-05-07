import tarfile
from subprocess import call
import os
import shutil
import re
from urllib import request

import log
from manage import parser

logger = log.factory(__name__)


def run(command, shell=False):
    call(command.split(), shell=shell)


def wget(url):
    run('wget {}'.format(url))


def add_apt_repository(repo):
    run('sudo add-apt-repository {}'.format(repo))


def perform_apt_get(item):
    run('sudo apt-get update')
    run('sudo apt-get install {}'.format(item))


def perform_apt_get_purge_remove(item):
    run('sudo apt-get --purge remove {}'.format(item))


def apt_get(func):
    def wrapper():
        func()
        perform_apt_get(func.__name__.replace('_', '-'))

    return wrapper


def extract_tar(src, dst):
    tar = tarfile.open(src, 'r:gz')
    tar.extractall(dst)
    tar.close()


# noinspection PyPep8Naming
class jetbrains:
    def __init__(self, code, platform='linux'):
        self.url = 'https://data.services.jetbrains.com/products/download?code={}&platform={}'.format(code, platform)

    def __call__(self, func):
        def wrapper():
            root = os.path.dirname(__file__)
            tar_filename = '{}.tar.gz'.format(func.__name__)

            src = os.path.join(root, tar_filename)
            dst = os.path.join(os.path.expanduser('~'), 'Applications')

            request.urlretrieve(self.url, src)
            
            os.makedirs(dst, exist_ok=True)
            extract_tar(src, dst)
            os.remove(src)

        return wrapper


# noinspection PyPep8Naming
class dependant_on:
    def __init__(self, *dependants):
        self.dependants = dependants

    def __call__(self, func):
        def wrapper():
            for dependant in self.dependants:
                dependant()
            func()

        return wrapper


def installable(func):
    parser.add_argument('--{}'.format(func.__name__), help=func.__doc__, action='store_true')
    return func
