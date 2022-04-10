#!/bin/bash
# Generate docs.md
# requires pydoc-markdown 4.6.1
readme_config=$(cat <<'EOF'
{
    "processors": [
        {
            "type": "filter"
        },
        {
            "type": "pydocmd"
        }
    ],
    "renderer": {
        "type": "markdown",
        "header_level_by_type": {
            "Module": 1,
            "Class": 3,
            "Method": 3,
            "Function": 3,
            "Variable": 3
        }
    }
}
EOF
)

toc_config=$(cat <<'EOF'
{
    "processors": [
        {
            "type": "filter"
        },
        {
            "type": "pydocmd"
        }
    ],
    "renderer": {
        "type": "markdown",
        "render_toc": true,
        "header_level_by_type": {
            "Module": 1,
            "Class": 3,
            "Method": 3,
            "Function": 3,
            "Variable": 3
        }
    }
}
EOF
)

parser_config=$(cat <<'EOF'
{
    "processors": [
        {
            "type": "filter",
            "expression": "not name == \"info\" and not name.startswith(\"_\") and default()"
        },
        {
            "type": "pydocmd"
        }
    ],
    "renderer": {
        "type": "markdown",
        "header_level_by_type": {
            "Module": 1,
            "Class": 3,
            "Method": 3,
            "Function": 3,
            "Variable": 3
        }
    }
}
EOF
)

cd jc
echo Building docs for: package
pydoc-markdown -m jc "${readme_config}" > ../docs/readme.md; echo "+++ package docs complete" &

echo Building docs for: lib
pydoc-markdown -m jc.lib "${toc_config}" > ../docs/lib.md; echo "+++ lib docs complete" &

echo Building docs for: utils
pydoc-markdown -m jc.utils "${toc_config}" > ../docs/utils.md; echo "+++ utils docs complete" &

echo Building docs for: streaming
pydoc-markdown -m jc.streaming "${toc_config}" > ../docs/streaming.md; echo "+++ streaming docs complete" &

echo Building docs for: universal parser
pydoc-markdown -m jc.parsers.universal "${toc_config}" > ../docs/parsers/universal.md; echo "+++ universal parser docs complete" &

# a bit of inception here... jc is being used to help
# automate the generation of its own documentation. :)

# pull jc parser objects into a bash array from jq
# filter out any plugin parsers
parsers=()
while read -r value
do
    parsers+=("$value")
done < <(jc -a | jq -c '.parsers[] | select(.plugin != true)')

for parser in "${parsers[@]}"
do (
    parser_name=$(jq -r '.name' <<< "$parser")
    compatible=$(jq -r '.compatible | join(", ")' <<< "$parser")
    version=$(jq -r '.version' <<< "$parser")
    author=$(jq -r '.author' <<< "$parser")
    author_email=$(jq -r '.author_email' <<< "$parser")

    echo "Building docs for: ${parser_name}"
    echo "[Home](https://kellyjonbrazil.github.io/jc/)" > ../docs/parsers/"${parser_name}".md
    pydoc-markdown -m jc.parsers."${parser_name}" "${parser_config}" >> ../docs/parsers/"${parser_name}".md
    echo "### Parser Information" >> ../docs/parsers/"${parser_name}".md
    echo "Compatibility:  ${compatible}" >> ../docs/parsers/"${parser_name}".md
    echo >> ../docs/parsers/"${parser_name}".md
    echo "Version ${version} by ${author} (${author_email})" >> ../docs/parsers/"${parser_name}".md
    echo "+++ ${parser_name} docs complete"
) &
done
wait
echo "Document Generation Complete"
