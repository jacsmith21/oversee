import os

import yaml


path = os.path.join(os.path.expanduser('~'), '.oversee.yaml')
with open(path) as f:
    oversee = yaml.load(f)

path = os.path.join(os.path.dirname(__file__), '.install.yaml')
with open(path) as f:
    install = yaml.load(f)

bash_aliases = oversee.get('bash_aliases', {})
move = oversee.get('move', {})
