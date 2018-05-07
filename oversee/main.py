import click

from oversee import terminal
from oversee import configure


@click.group()
def main():
    pass


@click.command()
@click.argument('name')
def install(name):
    """Installs a module defined in the .yaml file. Options include: {}"""
    terminal.install(name)


# noinspection PyUnresolvedReferences
install.help = install.__doc__.format(' '.join(configure.read_install().keys()))

main.add_command(install)


if __name__ == '__main__':
    main()
