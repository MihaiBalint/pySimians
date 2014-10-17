#!/usr/bin/env python
from __future__ import print_function

from fabric.api import local
from fabric.decorators import serial


@serial
def update_monkey_devices(
        repo="https://github.com/MihaiBalint/SimianArmy.git",
        temp_dir=None):

    if temp_dir is None:
        # TODO generate proper temp dir
        temp_dir = "temp"

    local("rm -rf {}".format(temp_dir))
    local("git clone {0} {1}".format(repo, temp_dir))
    local("mkdir -p scripts")
    local("mv {}/scripts/* scripts/ ".format(temp_dir))
    local("rm -rf {}".format(temp_dir))


@serial
def test_banana():
    print("TODO Error 404 no tests found")
