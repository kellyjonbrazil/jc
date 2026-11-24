#!/bin/bash
# Update all documentation (README.md, Man page, Doc files, llms-full.txt),
# the shell completion scripts, and the magic command table.
#
# Each step's output is saved and only shown if the step fails.
# Works with the bash 3.2 that ships with macOS.

logdir=$(mktemp -d)
trap 'rm -rf "$logdir"' EXIT

if [[ -t 1 && -z $NO_COLOR ]]; then
    bold=$'\e[1m'; dim=$'\e[2m'; green=$'\e[32m'; red=$'\e[31m'; reset=$'\e[0m'
else
    bold=''; dim=''; green=''; red=''; reset=''
fi

steps=0
failed=0
start=$SECONDS

# run_step <id> <command...>
# Run a step, saving its output, exit status, and run time in seconds.
run_step() {
    local id=$1
    shift
    local t0=$SECONDS
    "$@" > "$logdir/$id.log" 2>&1
    echo $? > "$logdir/$id.status"
    echo $((SECONDS - t0)) > "$logdir/$id.time"
}

# report <id> <label> [detail]
# Print a status line for a finished step, and the output of a failed step.
report() {
    local id=$1 label=$2 detail=$3
    local status time
    status=$(cat "$logdir/$id.status")
    time=$(cat "$logdir/$id.time")
    steps=$((steps + 1))

    if [[ $status -eq 0 ]]; then
        printf '  %s✓%s %-28s %s%3ss%s%s\n' "$green" "$reset" "$label" "$dim" "$time" "${detail:+  $detail}" "$reset"
    else
        printf '  %s✗ %-28s%s %s%3ss  failed%s\n' "$red" "$label" "$reset" "$dim" "$time" "$reset"
        # leave out docgen.sh's progress lines, so the errors stand out
        grep -v -e '^Building docs for: ' -e 'docs complete$' -e '^Document Generation ' \
            "$logdir/$id.log" | sed 's/^/      /'
        failed=$((failed + 1))
    fi
}

echo "${bold}Building documentation${reset}"
run_step readme ./readmegen.py &
run_step man ./mangen.py &
run_step llms ./llmsgen.py &
run_step docs ./docgen.sh &
wait

report readme 'README.md'
report man 'man page'
report llms 'llms-full.txt'
report docs 'docs/' "$(grep -c 'docs complete$' "$logdir/docs.log") files"

echo
echo "${bold}Building generated files${reset}"
run_step completions ./build-completions.py
report completions 'shell completions'
run_step magic ./build-magic-commands.py
report magic 'magic command table'

echo
total=$((SECONDS - start))
if [[ $failed -eq 0 ]]; then
    echo "${green}${bold}All $steps steps succeeded${reset} ${dim}in ${total}s${reset}"
else
    echo "${red}${bold}$failed of $steps steps failed${reset} ${dim}in ${total}s${reset}"
    exit 1
fi
