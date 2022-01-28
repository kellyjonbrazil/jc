#!/bin/bash
# system should be in "America/Los_Angeles" timezone for all tests to pass
# ensure no local plugin parsers are installed for all tests to pass

python3 -m unittest -v
