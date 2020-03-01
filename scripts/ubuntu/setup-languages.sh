#!/bin/bash

set -e

sudo apt-get install -y g++ gcc python2.7 openjdk-8-jdk openjdk-8-jre fpc perl octave

# # Ruby
sudo apt-add-repository -y ppa:brightbox/ruby-ng
sudo apt-get update -qq && sudo apt-get install -y ruby2.2
# if ! hash ruby 2>/dev/null
# then
#     sudo apt-get install -y autoconf bison build-essential libssl-dev libyaml-dev libreadline6-dev zlib1g-dev libncurses5-dev libffi-dev libgdbm3 libgdbm-dev
#     mkdir ruby
#     cd ruby
#     wget http://cache.ruby-lang.org/pub/ruby/2.2/ruby-2.2.0.tar.gz
#     tar xf ruby-2.2.0.tar.gz
#     cd ruby-2.2.0
#     ./configure --disable-install-doc
#     make
#     sudo make install
#     cd ../..
#     sudo rm -rf ruby
# fi

# JavaScript
#if [ $(uname -m) == 'x86_64' ]; then
#    # 64-bit stuff here
#    mkdir js
#    cd js
#    wget -q http://x.fleck.pw/mozjs-24_24-1_amd64.deb
#    dpkg -i mozjs-24_24-1_amd64.deb
#    sudo ln -s /usr/local/bin/js24 /usr/bin/js
#    cd ..
#    sudo rm -rf js
#elif ! hash js 2>/dev/null # For 32 bit, install from source
#then
#    mkdir js
#    cd js
#    wget https://ftp.mozilla.org/pub/mozilla.org/js/mozjs-24.2.0.tar.bz2
#    tar xf mozjs-24.2.0.tar.bz2
#    cd mozjs-24.2.0/js/src
#    ./configure
#    make
#    sudo make install
#    sudo ln -s /usr/local/bin/js24 /usr/bin/js
#    cd ../../../..
#    sudo rm -rf js
#fi

sudo apt-get install libmozjs-24-bin
sudo ln -s /usr/bin/js24 /usr/bin/js

# C# (Mono)
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
echo "deb http://download.mono-project.com/repo/debian wheezy main" | sudo tee /etc/apt/sources.list.d/mono-xamarin.list
sudo apt-get update -qq && sudo apt-get install -y mono-devel mono-complete
# mkdir cs
# cd cs
# git clone https://github.com/mono/mono.git
# cd mono
# ./autogen.sh --prefix /usr/local
# make
# sudo make install
# cd ../..
# rm -rf cs

