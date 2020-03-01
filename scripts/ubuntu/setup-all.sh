#!/bin/bash

set -e


BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
RELEASE=$(lsb_release -sc)
# Make sure Universe repository is being used
if ! apt-cache policy | grep -q "$RELEASE/universe"; then
    sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"
    sudo apt-get update -qq
fi

sudo apt-get install -y vim git-core libpq-dev libssl-dev libtool autoconf automake autotools-dev mono-complete wget tar
#sudo apt-get install -y python3.4 python3.4-dev libpython3.4 libpython3.4-dev
sudo apt-get install -y python3.5 python3.5-dev libpython3.5 libpython3.5-dev
sudo apt-get install -y build-essential gcc g++ python

# $BASE_DIR/setup-python3.3.sh

wget -q https://bootstrap.pypa.io/ez_setup.py -O - | sudo python3

sudo easy_install -U pip
sudo pip3 install virtualenv

$BASE_DIR/setup-languages.sh

