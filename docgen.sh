#!/bin/bash
# Generate markdown document files (*.md)
# Requires the yapf python library
# use ./docgen all to generate all docs

cd jc
(
    echo Building docs for: package
    ../doc2md.py jc > ../docs/readme.md && echo "+++ package docs complete" || echo "*** PACKAGE DOCS FAILED ***"
) &

(
    echo Building docs for: lib
    ../doc2md.py jc.lib > ../docs/lib.md && echo "+++ lib docs complete" || echo "*** LIB DOCS FAILED ***"
) &

(
    echo Building docs for: utils
    ../doc2md.py jc.utils > ../docs/utils.md && echo "+++ utils docs complete" || echo "*** UTILS DOCS FAILED ***"
) &

(
    echo Building docs for: streaming
    ../doc2md.py jc.streaming > ../docs/streaming.md && echo "+++ streaming docs complete" || echo "*** STREAMING DOCS FAILED ***"
) &

(
    echo Building docs for: universal parser
    ../doc2md.py jc.parsers.universal > ../docs/parsers/universal.md && echo "+++ universal parser docs complete" || echo "*** UNIVERSAL PARSER DOCS FAILED ***"
) &

# a bit of inception here... jc is being used to help
# automate the generation of its own documentation. :)

# pull jc parser objects into a bash array from jq
# filter out any plugin parsers
parsers=()
while read -r value
do
    parsers+=("$value")
done < <(jc -a | jq -c '.parsers[] | select(.plugin != true)')

for parser in "${parsers[@]}"; do
    parser_name=$(jq -r '.name' <<< "$parser")
        {
            if [[ $1 == "all" ]] || ! git diff --quiet --exit-code HEAD~5 -- "parsers/${parser_name}.py"; then
                echo "Building docs for: ${parser_name}"
                ../doc2md.py jc.parsers."${parser_name}" > ../docs/parsers/"${parser_name}".md && echo "+++ ${parser_name} docs complete" || echo "*** ${parser_name} DOCS FAILED ***"
            fi
        } &
done
wait
echo "Document Generation Complete"
