"""jc - JSON CLI output utility ipables Parser

Usage:
    Specify --iptables as the first argument if the piped input is coming from iptables

    Supports -vLn for all tables

Examples:

"""


class state():
    output = []
    chain = {}
    headers = []


def parse(data):
    cleandata = data.splitlines()

    for line in cleandata:

        if line.find('Chain') == 0:
            state.output.append(state.chain)
            state.chain = {}
            state.headers = []
            state.chain['rules'] = []

            parsed_line = line.split()

            state.chain['chain'] = parsed_line[1]
            state.chain['references'] = parsed_line[2].lstrip('(').rstrip(')').split()[0]

            continue

        if line.find('target') == 0:
            state.headers = []

            state.headers = [h for h in ' '.join(line.strip().split()).split() if h]
            state.headers.append("options")

            continue

        else:
            rule = line.split()
            temp_rule = {}
            for h, r in zip(state.headers, rule):
                temp_rule[h] = r
                state.chain['rules'].append(temp_rule)

                continue

    state.output = list(filter(None, state.output))

    return state.output
