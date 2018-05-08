#!/usr/bin/python3

import re
import os

from oversee.terminal import run


def move(src, dst):
    pattern = re.compile(r'([@\w]+):([@\w/]+)')

    matched = pattern.match(src)
    src_machine, src_path = matched.group(1), matched.group(2)

    matched = pattern.match(dst)
    dst_machine, dst_path = matched.group(1), matched.group(2)

    src_path, dst_path = [os.path.expanduser(path) for path in [src_path, dst_path]]

    command = 'scp -r {} {}'.format(convert_to_scp(src_machine, src_path), convert_to_scp(dst_machine, dst_path))
    run(command)


def convert_to_scp(loc, path):
    loc = known[loc]
    return '{}:{}'.format(loc, path) if loc else path



