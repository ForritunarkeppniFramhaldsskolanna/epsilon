#!/bin/bash

set -e

if ! hash python3.3 2>/dev/null
then
    mkdir python
    cd python

    sudo apt-get install -y libreadline-dev libsqlite3-dev libbz2-dev libgdbm-dev liblzma-dev libssl-dev

    wget -q http://www.python.org/ftp/python/3.3.4/Python-3.3.4.tgz
    tar xf Python-3.3.4.tgz
    cd Python-3.3.4

    ./configure
    make
    sudo make install

    cd ../../
    sudo rm -rf python
fi

