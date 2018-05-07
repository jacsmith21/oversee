from argparse import ArgumentParser

argparser = ArgumentParser()
args = {}


def add_argument(name, help=None, action='store_true'):
    argparser.add_argument(name, help=help, action=action)


def parse():
    global args
    args = vars(argparser.parse_args())


def contains(key):
    if not args:
        parse()

    return key in args


def get(key, default=None):
    if not args:
        parse()

    return args.get(key, default)


def items():
    if not args:
        parse()

    return args


def get_all():
    if not args:
        parse()

    return [arg for arg in args if args[arg]]
