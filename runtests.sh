#!/bin/bash
# system should be in "America/Los_Angeles" (PST8PDT) timezone for all tests
# to pass ensure no local plugin parsers are installed for all tests to pass

TZ=PST8PDT python3 -m unittest -v
