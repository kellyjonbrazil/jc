r"""jc - JSON Convert `nftables` command output parser

Parses `nft list ruleset`, `nft list tables`, and `nft list table <family>
<name>`, with or without the `-a` option. The result is a list with one
object per table, each holding its `chains`, `sets`, and `maps` lists.

A rule keeps the expression text exactly as `nft` prints it, minus the
trailing `# handle N` comment, so verdicts, anonymous sets, and counters
stay inside the `rule` string. Set and map `elements` are also kept as
printed. Named `counter`, `quota`, `flowtable`, and `ct` blocks are
skipped, and `-j`/`--json` input and output, `nft monitor`, and JSON-to-conf
are not supported.

Usage (cli):

    $ nft list ruleset | jc --nftables

or

    $ jc nft list ruleset

Usage (module):

    import jc
    result = jc.parse('nftables', nft_command_output)

Schema:

    [
      {
        "family":     string,
        "name":       string,
        "handle":     integer,        # [0]
        "comment":    string,         # [1]
        "flags": [
                        string
        ],
        "chains": [
          {
            "name":       string,
            "handle":     integer,    # [0]
            "type":       string,     # [2]
            "hook":       string,     # [1]
            "device":     string,     # [1]
            "priority":   string,     # [1]
            "policy":     string,     # [1]
            "comment":    string,     # [1]
            "rules": [
              {
                "rule":     string,
                "handle":   integer   # [0]
              }
            ]
          }
        ],
        "sets": [
          {
            "name":         string,
            "handle":       integer,  # [0]
            "type":         string,   # [3]
            "flags": [
                            string
            ],
            "timeout":      string,   # [1]
            "gc_interval":  string,   # [1]
            "size":         integer,  # [1]
            "policy":       string,   # [1]
            "auto_merge":   boolean,
            "counter":      boolean,
            "comment":      string,   # [1]
            "elements": [
                            string
            ]
          }
        ],
        "maps": [
          {
            # same fields as sets, plus:
            "value_type":   string   # [3]
          }
        ]
      }
    ]

    [0] null unless `-a` was used
    [1] null if not set
    [2] null for a regular chain
    [3] the `typeof` expression when the set or map is declared with
        `typeof` instead of `type`

Examples:

    $ nft -a list ruleset | jc --nftables -p
    [
      {
        "family": "inet",
        "name": "filter",
        "handle": 1,
        "comment": null,
        "flags": [],
        "chains": [
          {
            "name": "input",
            "handle": 1,
            "type": "filter",
            "hook": "input",
            "device": null,
            "priority": "filter",
            "policy": "drop",
            "comment": null,
            "rules": [
              {
                "rule": "ct state established,related accept",
                "handle": 4
              },
              {
                "rule": "tcp dport 8080 counter packets 12 bytes 720 accept",
                "handle": 8
              }
            ]
          }
        ],
        "sets": [],
        "maps": []
      },
      ...
    ]

    $ nft list tables | jc --nftables -p
    [
      {
        "family": "inet",
        "name": "filter",
        "handle": null,
        "comment": null,
        "flags": [],
        "chains": [],
        "sets": [],
        "maps": []
      },
      ...
    ]
"""
import re
from typing import Dict, Iterator, List, Optional, Tuple
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`nftables` command parser'
    author = 'Tung Lam'
    author_email = '53996158+tunglambk@users.noreply.github.com'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['nft']


__version__ = info.version

# `nft -a` prints the object handle as a trailing comment
_handle_pattern = re.compile(r'\s*#\s*handle\s+(?P<handle>\d+)\s*$')

_table_pattern = re.compile(r'^table\s+(?P<family>\S+)\s+(?P<name>\S+)\s*\{?$')
_named_block_pattern = re.compile(r'^(?P<kind>chain|set|map|counter|quota|flowtable)\s+(?P<name>\S+)\s*\{$')
_ct_block_pattern = re.compile(r'^ct\s+(?:helper|timeout|expectation)\s+\S+\s*\{$')

_chain_type_pattern = re.compile(r'^type\s+(?P<type>\S+)')
_hook_pattern = re.compile(r'\bhook\s+(?P<hook>\S+)')
_device_pattern = re.compile(r'\bdevice\s+(?P<device>"[^"]*"|\S+)')
_priority_pattern = re.compile(r'\bpriority\s+(?P<priority>.+?);')
_policy_pattern = re.compile(r'\bpolicy\s+(?P<policy>[^;]+)')


def _split_handle(statement: str) -> Tuple[str, Optional[str]]:
    """
    Split the trailing `# handle N` comment from a statement. Returns the
    statement and the handle string, or `None` when there is no handle.
    """
    match = _handle_pattern.search(statement)

    if match:
        return statement[:match.start()].strip(), match.group('handle')

    return statement.strip(), None


def _brace_depth(text: str) -> int:
    """
    Return the net number of open braces in a statement, ignoring braces that
    appear inside a quoted string.
    """
    depth = 0
    in_quotes = False

    for char in text:
        if char == '"':
            in_quotes = not in_quotes
        elif not in_quotes:
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1

    return depth


def _is_block_declaration(statement: str) -> bool:
    """
    Return `True` when the statement opens a `{ }` block.
    """
    if not statement.endswith('{'):
        return False

    return bool(
        _table_pattern.match(statement)
        or _named_block_pattern.match(statement)
        or _ct_block_pattern.match(statement)
    )


def _statements(data: str) -> Iterator[Tuple[str, Optional[str]]]:
    """
    Yield `(statement, handle)` pairs. Lines that wrap inside `{ }`, such as
    a long `elements = { ... }` list, are joined into a single statement.
    """
    pending = ''

    for line in data.splitlines():
        line = line.strip()

        if not line:
            continue

        pending = f'{pending} {line}' if pending else line
        statement, handle = _split_handle(pending)

        # a block declaration or a closing brace is complete even though its
        # brace is unbalanced
        if statement == '}':
            yield statement, handle
            pending = ''
            continue

        if _is_block_declaration(statement):
            yield statement, handle
            pending = ''
            continue

        if _brace_depth(pending) == 0:
            yield statement, handle
            pending = ''


def _comment_value(statement: str) -> str:
    """Return the text of a `comment "..."` statement without the quotes."""
    return statement[len('comment '):].strip().strip('"')


def _new_table(family: str, name: str, handle: Optional[str]) -> JSONDictType:
    """Create an empty table object."""
    return {
        'family': family,
        'name': name,
        'handle': handle,
        'comment': None,
        'flags': [],
        'chains': [],
        'sets': [],
        'maps': []
    }


def _new_chain(name: str, handle: Optional[str]) -> JSONDictType:
    """Create an empty chain object."""
    return {
        'name': name,
        'handle': handle,
        'type': None,
        'hook': None,
        'device': None,
        'priority': None,
        'policy': None,
        'comment': None,
        'rules': []
    }


def _new_set(name: str, handle: Optional[str], is_map: bool) -> JSONDictType:
    """Create an empty set or map object."""
    entry: JSONDictType = {
        'name': name,
        'handle': handle,
        'type': None
    }

    if is_map:
        entry['value_type'] = None

    entry.update({
        'flags': [],
        'timeout': None,
        'gc_interval': None,
        'size': None,
        'policy': None,
        'auto_merge': False,
        'counter': False,
        'comment': None,
        'elements': []
    })

    return entry


def _split_elements(statement: str) -> List[str]:
    """
    Split the body of an `elements = { ... }` statement on commas that are
    not inside a quoted string.
    """
    body = statement[statement.index('{') + 1:statement.rindex('}')]
    elements = []
    current = ''
    in_quotes = False

    for char in body:
        if char == '"':
            in_quotes = not in_quotes
            current += char
        elif char == ',' and not in_quotes:
            if current.strip():
                elements.append(current.strip())
            current = ''
        else:
            current += char

    if current.strip():
        elements.append(current.strip())

    return elements


def _parse_chain_line(chain: JSONDictType, statement: str, handle: Optional[str]) -> None:
    """
    Parse a line inside a chain block. The chain header line starts with
    `type` and carries the hook, priority, and policy; a standalone `comment`
    line is the chain comment; everything else is a rule.
    """
    if statement.startswith('comment '):
        chain['comment'] = _comment_value(statement)
        return

    if statement.startswith('type ') and ' hook ' in statement:
        type_match = _chain_type_pattern.match(statement)
        hook_match = _hook_pattern.search(statement)
        device_match = _device_pattern.search(statement)
        priority_match = _priority_pattern.search(statement)
        policy_match = _policy_pattern.search(statement)

        if type_match:
            chain['type'] = type_match.group('type')

        if hook_match:
            chain['hook'] = hook_match.group('hook')

        if device_match:
            chain['device'] = device_match.group('device').strip('"')

        if priority_match:
            chain['priority'] = priority_match.group('priority').strip()

        if policy_match:
            chain['policy'] = policy_match.group('policy').strip()

        return

    chain['rules'].append({
        'rule': statement,
        'handle': handle
    })


def _parse_set_line(entry: JSONDictType, statement: str, is_map: bool) -> None:
    """
    Parse a property line inside a set or map block. Unrecognized properties
    are ignored.
    """
    if statement.startswith('type ') or statement.startswith('typeof '):
        value = statement.split(' ', 1)[1].strip()

        if is_map and ' : ' in value:
            key_type, value_type = value.split(' : ', 1)
            entry['type'] = key_type.strip()
            entry['value_type'] = value_type.strip()
        else:
            entry['type'] = value

    elif statement.startswith('flags '):
        entry['flags'] = [flag.strip() for flag in statement[len('flags '):].split(',') if flag.strip()]

    elif statement == 'counter':
        entry['counter'] = True

    elif statement.startswith('comment '):
        entry['comment'] = _comment_value(statement)

    elif statement.startswith('elements = '):
        entry['elements'] = _split_elements(statement)

    elif statement.startswith('timeout '):
        entry['timeout'] = statement[len('timeout '):].strip()

    elif statement.startswith('gc-interval '):
        entry['gc_interval'] = statement[len('gc-interval '):].strip()

    elif statement.startswith('size '):
        entry['size'] = statement[len('size '):].strip()

    elif statement.startswith('policy '):
        entry['policy'] = statement[len('policy '):].strip()

    elif statement == 'auto-merge':
        entry['auto_merge'] = True


def _parse_table_line(table: JSONDictType, statement: str) -> None:
    """
    Parse a property line inside a table block. Only the table `comment` and
    `flags` are captured; anything else is ignored.
    """
    if statement.startswith('comment '):
        table['comment'] = _comment_value(statement)

    elif statement.startswith('flags '):
        table['flags'] = [flag.strip() for flag in statement[len('flags '):].split(',') if flag.strip()]


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for table in proc_data:
        table['handle'] = jc.utils.convert_to_int(table['handle'])

        for chain in table['chains']:
            chain['handle'] = jc.utils.convert_to_int(chain['handle'])

            for rule in chain['rules']:
                rule['handle'] = jc.utils.convert_to_int(rule['handle'])

        for entry in table['sets'] + table['maps']:
            entry['handle'] = jc.utils.convert_to_int(entry['handle'])
            entry['size'] = jc.utils.convert_to_int(entry['size'])

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[JSONDictType] = []
    stack: List[Tuple[str, JSONDictType]] = []

    if jc.utils.has_data(data):

        for statement, handle in _statements(data):

            if statement == '}':
                if stack:
                    stack.pop()
                continue

            table_match = _table_pattern.match(statement)

            if table_match:
                table = _new_table(table_match.group('family'), table_match.group('name'), handle)
                raw_output.append(table)

                if statement.endswith('{'):
                    stack = [('table', table)]

                continue

            if not stack:
                continue

            named_match = _named_block_pattern.match(statement)

            if named_match:
                # only chain, set, and map blocks are captured. Anything else
                # keeps its own entry on the stack so its contents are skipped
                # until the matching closing brace.
                if stack[-1][0] != 'table':
                    stack.append(('ignored', {}))
                    continue

                kind = named_match.group('kind')
                name = named_match.group('name')
                table = stack[-1][1]

                if kind == 'chain':
                    chain = _new_chain(name, handle)
                    table['chains'].append(chain)
                    stack.append(('chain', chain))

                elif kind in ('set', 'map'):
                    entry = _new_set(name, handle, is_map=kind == 'map')
                    table['sets' if kind == 'set' else 'maps'].append(entry)
                    stack.append((kind, entry))

                else:
                    stack.append(('ignored', {}))

                continue

            if _ct_block_pattern.match(statement):
                stack.append(('ignored', {}))
                continue

            kind, current = stack[-1]

            if kind == 'table':
                _parse_table_line(current, statement)

            elif kind == 'chain':
                _parse_chain_line(current, statement, handle)

            elif kind == 'set':
                _parse_set_line(current, statement, is_map=False)

            elif kind == 'map':
                _parse_set_line(current, statement, is_map=True)

    return raw_output if raw else _process(raw_output)
