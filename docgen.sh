#!/bin/bash
# Generate markdown document files (*.md)
# Requires the yapf python library
#
# Parser docs are only built when the doc is missing or older than its parser
# or doc2md.py. Use ./docgen.sh all to build all docs (e.g. after a fresh
# clone, where all files get the same timestamp).

# the background jobs, so their exit status can be checked
pids=()

# build_doc <module> <doc file> <name>
# Write the doc to a temporary file and move it into place only if doc2md.py
# succeeds, so a failed build never leaves a partial doc that looks up to date.
build_doc() {
    local module=$1 doc=$2 name=$3
    echo "Building docs for: ${name}"
    if ../doc2md.py "$module" > "${doc}.tmp"; then
        mv "${doc}.tmp" "$doc"
        echo "+++ ${name} docs complete"
    else
        rm -f "${doc}.tmp"
        echo "*** ${name} DOCS FAILED ***"
        return 1
    fi
}

cd jc || exit 1

build_doc jc ../docs/readme.md package &
pids+=($!)
build_doc jc.lib ../docs/lib.md lib &
pids+=($!)
build_doc jc.utils ../docs/utils.md utils &
pids+=($!)
build_doc jc.streaming ../docs/streaming.md streaming &
pids+=($!)
build_doc jc.parsers.universal ../docs/parsers/universal.md 'universal parser' &
pids+=($!)

# a bit of inception here... jc is being used to help
# automate the generation of its own documentation. :)

# pull jc parser names into a bash array from jq
# filter out any plugin parsers
parsers=()
while read -r value
do
    parsers+=("$value")
done < <(jc -a | jq -r '.parsers[] | select(.plugin != true) | .name')

for parser_name in "${parsers[@]}"; do
    doc="../docs/parsers/${parser_name}.md"
    if [[ $1 == "all" || ! -f $doc || parsers/${parser_name}.py -nt $doc || ../doc2md.py -nt $doc ]]; then
        build_doc "jc.parsers.${parser_name}" "$doc" "$parser_name" &
        pids+=($!)
    fi
done

# exit 1 if any job failed
failed=0
for pid in "${pids[@]}"; do
    wait "$pid" || failed=1
done

if [[ $failed -eq 0 ]]; then
    echo "Document Generation Complete"
else
    echo "Document Generation Failed"
fi
exit $failed
