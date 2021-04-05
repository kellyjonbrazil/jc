#!/bin/bash
# Update all documentation (README.md, Man page, Doc files)

./readmegen.py
./mangen.py
./docgen.sh
