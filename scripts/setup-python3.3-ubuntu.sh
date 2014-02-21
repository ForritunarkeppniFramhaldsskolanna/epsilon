
mkdir python33
cd python33

sudo apt-get install libreadline-dev libsqlite3-dev libbz2-dev libgdbm-dev liblzma-dev

wget http://www.python.org/ftp/python/3.3.4/Python-3.3.4.tgz
tar xvf Python-3.3.4.tgz
cd Python-3.3.4

./configure
make
sudo make install

cd ..
rm -rf python33

