#!/bin/bash
# system should be in "America/Los_Angeles" timezone for all tests to pass
# ensure no local plugin parsers are installed for all tests to pass

pip uninstall pygments ruamel.yaml xmltodict --yes
python3 -m unittest -v
pip install pygments ruamel.yaml xmltodict
