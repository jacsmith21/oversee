import os
import re
import subprocess
import tarfile

import click
import elevate

from oversee import config


def install(name):
    commands = config.install[name]
    for command in commands:
        interpret(command, name)


def interpret(command, name):
        if isinstance(command, dict):
            for key in command:
                COMMANDS[key](command[key])
        else:
            try:
                COMMANDS[command](name)
            except KeyError:
                run(command)


def run(command, background=False):
    commands = command.split('|')

    stdin = None
    for command in commands:
        command = command.split()
        if background:
            process = subprocess.Popen(command, stdin=stdin)
        else:
            process = subprocess.call(command, stdin=stdin)
        stdin = process.stdout


def add_apt_repository(repo):
    run('sudo add-apt-repository {}'.format(repo))


def apt_get(item):
    run('sudo apt-get update')
    run('sudo apt-get install {}'.format(item))


def jetbrains(code):
    url = 'https://data.services.jetbrains.com/products/download?code={}&platform=linux'.format(code)
    root = os.path.dirname(__file__)
    tar_filename = '{}.tar.gz'.format(code)

    src = os.path.join(root, '.temp', tar_filename)
    dst = os.path.join(os.path.expanduser('~'), 'Applications')

    elevate.file.download(url, src)

    os.makedirs(dst, exist_ok=True)
    tar = tarfile.open(src, 'r:gz')
    tar.extractall(dst)

    folder = os.path.commonprefix(tar.getnames())
    folder = folder.lower()

    tar.close()
    os.remove(src)

    if not folder:
        raise ValueError('No common prefix found within {}. Extracted files remain in {}!'.format(src, dst))

    application, _ = folder.split('-')
    run(os.path.join(dst, folder, 'bin', '{}.sh'.format(application)), background=True)


COMMANDS = {'apt-get': apt_get, 'install': install, 'repository': add_apt_repository, 'jetbrains': jetbrains}


def scp(src, dst):
    pattern = re.compile(r'(?:([~@.\w]+):)?([~@.\w/]+)')

    matched = pattern.match(src)
    src_machine, src_path = matched.group(1), matched.group(2)

    matched = pattern.match(dst)
    dst_machine, dst_path = matched.group(1), matched.group(2)

    def convert_to_scp(machine, path):
        if machine is not None:
            host = config.move['hosts'][machine]
            user, _ = host.split('@')
            path = path.replace('~', '/home/{}'.format(user))
            return '{}:{}'.format(host, path) if machine else path
        else:
            return os.path.expanduser(path)

    key = config.move['key']
    key = os.path.expanduser(key)

    if not os.path.exists(key):
        raise FileNotFoundError('Key does not exist: {}'.format(key))

    command = 'scp -i {} -r {} {}'.format(key, convert_to_scp(src_machine, src_path), convert_to_scp(dst_machine, dst_path))
    click.echo(command)
    run(command)


def export_aliases():
    with open('/home/jacob/.bash_aliases', 'w') as f:

        bash_aliases = ''
        for alias, command in config.bash_aliases.get('aliases', {}).items():
            bash_aliases += 'alias {}="{}"\n'.format(alias, command)

        bash_aliases += '\n'
        for link in config.bash_aliases.get('links', []):
            bash_aliases += 'sudo ln -sf {} {}\n'.format(link['that'], link['this'])

        bash_aliases += '\n'
        for name, lines in config.bash_aliases.get('functions', {}).items():
            bash_aliases += '{}()'.format(name)
            bash_aliases += ' {\n'
            for line in lines:
                bash_aliases += '    {}\n'.format(line)
        bash_aliases += '}\n'

        bash_aliases += '\n'
        for name, export in config.bash_aliases.get('exports', {}).items():
            export = os.path.expanduser(export)
            export = export.rstrip('\n')
            bash_aliases += 'export {}="{}"\n'.format(name, export)

        bash_aliases += '\n'
        for path in config.bash_aliases.get('keys', []):
            path = os.path.expanduser(path)
            bash_aliases += 'ssh-add {}\n'.format(path)

        bash_aliases += '\n'
        for source in config.bash_aliases.get('sources', []):
            source = os.path.expanduser(source)

            if not os.path.exists(source):
                click.echo('{} does not exist. Skipping source!'.format(source))
                continue

            bash_aliases += 'source {}\n'.format(source)

        f.write(bash_aliases)
