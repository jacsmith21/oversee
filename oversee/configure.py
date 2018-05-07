import os

import yaml


def read(path):
    with open(path) as f:
        return yaml.load(f)


def read_install():
    path = os.path.join(os.path.dirname(__file__), '..', 'defaults', 'install.yaml')
    return read(path)
