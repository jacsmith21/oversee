import os
import re

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


aliases = {}
for key in oversee:
    if key.endswith('_aliases'):
        aliases[re.match(r'(\w+)_aliases', key).group(1)] = oversee.get(key)

jetbrains = oversee.get('jetbrains', {})
environments = oversee.get('environments', {})
