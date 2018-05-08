import os
import subprocess
import tarfile
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
