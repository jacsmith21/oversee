import os
import shutil

import click
import git

from oversee import terminal, jetbrains, extensions
from oversee import config


@click.group()
def main():
    pass


@click.command()
@click.argument('name')
@list_option(config.install.keys())
def install(name):
    """Installs a module defined in the .yaml file. Options include: {}"""
    terminal.install(name)


@click.command()
@click.argument('src')
@click.argument('dst')
def move(src, dst):
    """Moves a file / folder from one location to another using scp!"""
    terminal.scp(src, dst)


@click.command()
@click.argument('name', required=False)
@click.option('-ls', help='List the available options!', is_flag=True)
@extensions.validate(required='name', unless='ls')
def export(name, ls):
    """Exports your bash aliases to .bash_aliases!"""
    if ls:
        click.echo('\n'.join(config.aliases.keys()))
        return

    terminal.export_aliases(name)


@click.command()
@click.argument('name', required=False)
@click.option('-ls', help='List the available options!', is_flag=True)
@extensions.validate(required='name', unless='ls')
def sync(name, ls):
    """Sync you a specific IDE with your saved settings!"""
    if ls:
        click.echo('\n'.join(jetbrains.options()))
        return

    jetbrains_root = jetbrains.get_path(name)
    click.echo('Syncing settings to {}'.format(jetbrains_root))

    path = os.path.join(jetbrains_root, 'config')
    for file in config.jetbrains:
        dst = os.path.join(path, file)
        src = os.path.join(os.path.expanduser('~'), '.oversee', 'jetbrains', file)
        if not os.path.exists(src):
            click.echo('{} does not exist and is not being synced.')
        else:
            click.echo('Copying {} to {}'.format(file, dst))

        shutil.copy(src, dst)


@click.command()
@click.argument('name', required=False)
@click.option('-ls', help='List the available options!', is_flag=True)
@extensions.validate(required='name', unless='ls')
def save(name, ls):
    """Save your the settings of a jetbrains IDE to a common location so they can be synced with the other IDEs."""
    if ls:
        click.echo('\n'.join(jetbrains.options()))
        return

    path = jetbrains.get_path(name)
    click.echo('Saving settings from {}'.format(path))

    directory = os.path.join(path, 'config')
    for file in config.jetbrains:
        src = os.path.join(directory, file)
        dst = os.path.join(os.path.expanduser('~'), '.oversee', 'jetbrains', file)
        if not os.path.exists(src):
            click.echo('{} does not exist and is not being saved.')
        else:
            click.echo('Copying {} to {}'.format(file, dst))

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)


@click.command()
@click.argument('name', required=False)
@click.option('-ls', help='List the available options!', is_flag=True)
@extensions.validate(required='name', unless='ls')
def setup(name, ls):
    """Setup an environment!"""
    if ls:
        click.echo('\n'.join(config.environments.keys()))
        return

    if name not in config.environments:
        click.echo('{} does not exist :('.format(name))
        return
    else:
        click.echo('Setting up {}!'.format(name))

    environment = config.environments[name]
    for item in environment.get('install', []):
        terminal.install(item)

    for repository in environment.get('clone', []):
        url = repository['repository']
        dst = repository['to']
        dst = os.path.expanduser(dst)
        name, _ = os.path.basename(url).split('.')
        click.echo('Cloning {} to {}'.format(name, dst))

        to_path = os.path.join(dst, name)
        os.makedirs(dst, exist_ok=True)
        git.Repo.clone_from(url, to_path=to_path)


# noinspection PyUnresolvedReferences
install.help = install.__doc__.format(' '.join(config.install.keys()))

main.add_command(install)
main.add_command(move)
main.add_command(export)
main.add_command(save)
main.add_command(sync)
main.add_command(setup)


if __name__ == '__main__':
    main()
