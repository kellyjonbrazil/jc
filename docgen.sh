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

# pull jc parser objects into a bash array from jq
parsers=()
while read -r value
do
  parsers+=("$value")
done < <(jc -a | jq -c '.parsers[]')

# iterate over the bash array
for parser in "${parsers[@]}"
do
    # pydocmd simple jc.parsers.${parser}+ > ../docs/parsers/${parser}.md
    parser_name=$(echo -e "$parser" | jq -r '.name' )
    compatible=$(echo -e "$parser" | jq -r '.compatible | join(", ")')
    version=$(echo -e "$parser" | jq -r '.version')
    author=$(echo -e "$parser" | jq -r '.author')
    author_email=$(echo -e "$parser" | jq -r '.author_email')

    echo "Building docs for: ${parser_name}"
    pydocmd simple jc.parsers."${parser_name}"+ > ../docs/parsers/"${parser_name}".md
    echo "Compatibility:  ${compatible}" >> ../docs/parsers/"${parser_name}".md
    echo >> ../docs/parsers/"${parser_name}".md
    echo "Version ${version} by ${author} (${author_email})" >> ../docs/parsers/"${parser_name}".md
done
