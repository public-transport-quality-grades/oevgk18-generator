#!/bin/bash

sudo apt-get install -y curl g++ make

curl -L http://download.osgeo.org/libspatialindex/spatialindex-src-1.8.5.tar.gz | tar xz

cd spatialindex-src-1.8.5

./configure

make

sudo make install

# make sure the library will be found
sudo ldconfig
