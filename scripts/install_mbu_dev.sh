#!/bin/bash
set -e
VER=2.1
export SOURCEDIR=/src
sudo sed -i "s;/usr/local/bin/python;/usr/local/components/MBU-${VER}/bin/python3.7;g" /usr/local/components/MBU-${VER}/lib/python3.7/cgi.py
# export DEST_DIR=/usr/local/components/MBU-2.0
# sudo $PIP install toolz==0.10.0 && \
# sudo $PIP install pyproj==2.5.0 && \
# sudo $PIP install pyparsing==2.4.6 && \
# sudo $PIP install Pillow==5.4.1 && \
# sudo $PIP install pbr==5.4.4 && \
# sudo $PIP install matplotlib==2.0.0 && \
#sudo $PIP install --no-binary :all: cython
#sudo $PIP install --no-deps --no-binary :all: cftime==1.3.1
sudo $PIP install --no-deps --no-binary :all: netcdf4==1.4.0
# sudo $PIP install Logbook==1.5.3 && \
# sudo $PIP install iso8601==0.1.12 && \
# sudo $PIP install funcsigs==1.0.2 && \
#sudo $PIP install --no-binary :all: dateutils==0.6.11
sudo $PIP install --no-binary :all: configobj==5.0.6
# sudo $PIP install pyFFTW
sudo $PIP install -e /src/

