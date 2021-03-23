#!/bin/bash

python3 -m unittest -v

echo
echo "Running local-only tests:"
echo

python3 -m unittest tests.localtest_last -v
python3 -m unittest tests.localtest_date -v
