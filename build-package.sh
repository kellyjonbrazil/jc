#!/bin/bash
# build jc PIP package
# to install locally, run:   pip3 install jc-x.x.tar.gz

python3 setup.py sdist bdist_wheel
