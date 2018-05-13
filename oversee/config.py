import os

import yaml


path = os.path.join(os.path.expanduser('~'), '.oversee.yaml')
with open(path) as f:
    oversee = yaml.load(f)

path = os.path.join(os.path.dirname(__file__), '.install.yaml')
with open(path) as f:
    install = yaml.load(f)

move = oversee.get('move', {})


def get_aliases(name):
    return oversee.get('{}_aliases'.format(name))


jetbrains = oversee.get('jetbrains', {})
