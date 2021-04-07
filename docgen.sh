#!/bin/bash
# Generate docs.md
# requires pydoc-markdown 2.1.0.post1

cd jc
echo Building docs for: package
pydocmd simple jc+ > ../docs/readme.md
echo Building docs for: utils
pydocmd simple utils+ > ../docs/utils.md

# a bit of inception here... jc is being used to help
# automate the generation of its own documentation. :)

parsers=$(jc -a | jq -r .parsers[].name)

for parser in $parsers
do
    echo Building docs for: $parser
    pydocmd simple jc.parsers.${parser}+ > ../docs/parsers/${parser}.md
done
