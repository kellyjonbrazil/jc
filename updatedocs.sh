#!/bin/bash
# Update all documentation (README.md, Man page, Doc files)

echo === Building README.md
./readmegen.py && echo "+++ README.md build successful" || echo "--- README.md build failed"
echo === Building man page
./mangen.py && echo "+++ man page build successful" || echo "--- man page build failed"
echo === Building documentation
./docgen.sh && echo "+++ documentation build successful" || echo "--- documentation build failed"
