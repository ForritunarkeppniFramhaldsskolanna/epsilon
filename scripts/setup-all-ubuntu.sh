#!/bin/bash

./setup-python3.3-ubuntu.sh

wget http://python-distribute.org/distribute_setup.py
sudo python3.3 distribute_setup.py
sudo rm distribute_setup.py

sudo easy_install -U pip
sudo pip3.3 install virtualenv

# sudo apt-get install python3-setuptools python3-pip python-virtualenv

