import os

import yaml

defaults = os.path.join(os.path.dirname(__file__), '..', 'defaults')

path = os.path.join(defaults, 'install.yaml')
with open(path) as f:
    install = yaml.load(f)

path = os.path.join(defaults, 'bash_aliases.yaml')
with open(path) as f:
    bash_aliases = yaml.load(f)

path = os.path.join(os.path.expanduser('~'), '.oversee', 'move.yaml')
with open(path) as f:
    move = yaml.load(f)
