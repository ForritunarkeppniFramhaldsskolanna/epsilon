#!/bin/bash

set -e

if ! hash jk_init 2>/dev/null
then
    mkdir jailkit
    cd jailkit
    wget http://olivier.sessink.nl/jailkit/jailkit-2.17.tar.bz2
    tar xf jailkit-2.17.tar.bz2
    cd jailkit-2.17
    ./configure
    make
    sudo make install
    cd ../..
    sudo rm -rf jailkit
fi
