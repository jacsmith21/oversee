import click

from oversee import terminal
from oversee import config


@click.group()
def main():
    pass


@click.command()
@click.argument('name')
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
def export():
    """Exports your bash aliases to .bash_aliases!"""
    terminal.export_aliases()


# noinspection PyUnresolvedReferences
install.help = install.__doc__.format(' '.join(config.install.keys()))

main.add_command(install)
main.add_command(move)
main.add_command(export)


if __name__ == '__main__':
    main()
