import os

import yaml

path = os.path.join(os.path.dirname(__file__), '..', 'defaults', 'install.yaml')
with open(path) as f:
    install = yaml.load(f)
