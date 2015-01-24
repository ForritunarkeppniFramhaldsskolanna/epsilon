#!/bin/bash

set -e

# Make sure Universe repository is being used
sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"
sudo apt-get update

sudo apt-get install -y vim git-core libpq-dev libssl-dev libtool autoconf automake autotools-dev mono-gmcs
sudo apt-get install python3.4 python3.4-dev libpython3.4 libpython3.4-dev

#./setup-python3.3.sh
./setup-jailkit.sh

#wget http://python-distribute.org/distribute_setup.py
sudo python3 distribute_setup.py
#sudo rm distribute_setup.py
sudo rm distribute-*.tar.gz

sudo easy_install -U pip
sudo pip3 install virtualenv

./setup-languages.sh

