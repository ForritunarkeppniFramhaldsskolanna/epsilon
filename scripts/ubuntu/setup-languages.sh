#!/bin/bash

set -e

sudo apt-get install -y g++ gcc python2.7 openjdk-7-jdk openjdk-7-jre fpc perl octave

# Ruby
if ! hash ruby 2>/dev/null
then
    mkdir ruby
    cd ruby
    wget http://cache.ruby-lang.org/pub/ruby/2.1/ruby-2.1.1.tar.gz
    tar xf ruby-2.1.1.tar.gz
    cd ruby-2.1.1
    ./configure
    make
    sudo make install
    cd ../..
    sudo rm -rf ruby
fi

# JavaScript
if ! hash js 2>/dev/null
then
    mkdir js
    cd js
    wget https://ftp.mozilla.org/pub/mozilla.org/js/mozjs-24.2.0.tar.bz2
    tar xf mozjs-24.2.0.tar.bz2
    cd mozjs-24.2.0/js/src
    ./configure
    make
    sudo make install
    sudo ln -s /usr/local/bin/js24 /usr/bin/js
    cd ../../../..
    sudo rm -rf js
fi

# C#
mkdir cs
cd cs
git clone https://github.com/mono/mono.git
cd mono
./autogen.sh --prefix /usr/local
make
sudo make install
cd ../..
rm -rf cs

