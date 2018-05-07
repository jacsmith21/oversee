def alias(func):
    def wrapper():
        return 'alias {}="{}"'.format(func.__name__, func())

    return wrapper


def link(func):
    def wrapper():
        return 'sudo ln -sf {} {}'.format(*func())

    return wrapper


@alias
def tb_default():
    return 'tensorboard --logdir=TRAIN:training,VALIDATION:summary'

@alias
def which_vga():
    return 'lspci -vnnn | perl -lne \'print if /^\d+\:.+(\[\S+\:\S+\])/\' | grep VGA'


@alias
def rollback():
    return 'setxkbmap -option'


@alias
def swap():
    return 'setxkbmap -option altwin:swap_alt_win'


@alias
def startup():
    return 'subl ~/.bash_aliases'


@alias
def restart():
    return 'source ~/.bashrc'


@alias
def scratch():
    return 'cd ~/scratch'


@link
def node():
    return '/usr/local/n/versions/node/9.4.0/bin/node', '/usr/bin/nodejs'


@link
def cmake():
    return '/usr/local/bin/cmake', '/usr/bin/cmake'
