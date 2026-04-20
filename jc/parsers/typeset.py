r"""jc - JSON Convert `typeset` and `declare` Bash internal command output parser

Convert `typeset` and `declare` bash internal commands with no options or the
following:  `-a`, `-A`, `-i`, `-l`, `-p`, `-r`, `-u`, and `-x`

Note: function parsing is not supported (e.g. `-f` or `-F`)

Usage (cli):

    $ typeset | jc --typeset

Usage (module):

    import jc
    result = jc.parse('typeset', typeset_command_output)

Schema:

    [
      {
        "name":         string,
        "value":        string/integer/array/object/null,    # [0]
        "type":         string,                              # [1]
        "readonly":     boolean/null,
        "integer":      boolean/null,
        "lowercase":    boolean/null,
        "uppercase":    boolean/null,
        "exported":     boolean/null
      }
    ]

    Key/value pairs other than `name`, `value`, and `type` will only be non-null
    when the information is available from the `typeset` or `declare` output.

    If declare options are not given to `jc` within the `typeset` output, then
    it will assume all arrays are simple `array` type.

    [0] Based on type. `variable` type is null if not set, a string when the
        bash variable is set unless the `integer` field is set to `True`, then
        the type is integer. `array` type is an array of strings or integers as
        above. `associative` type is an object of key/value pairs where values
        are strings or integers as above. Objects have the schema of:

        {
          "<key1>": string/integer,
          "<key2>": string/integer
        }

    [1] Possible values: `variable`, `array`, or `associative`

Examples:

    $ typeset -p | jc --typeset -p
    [
      {
        "name": "associative_array",
        "value": {
          "key2": "abc",
          "key3": "1 2 3",
          "key1": "hello \"world\""
        },
        "type": "associative",
        "readonly": false,
        "integer": false,
        "lowercase": false,
        "uppercase": false,
        "exported": false
      },
      {
        "name": "integers_associative_array",
        "value": {
          "one": 1,
          "two": 500,
          "three": 999
        },
        "type": "associative",
        "readonly": false,
        "integer": true,
        "lowercase": false,
        "uppercase": false,
        "exported": false
      }
    ]

    $ typeset -p | jc --typeset -p -r
    [
      {
        "name": "associative_array",
        "value": {
          "key2": "abc",
          "key3": "1 2 3",
          "key1": "hello \"world\""
        },
        "type": "associative",
        "readonly": false,
        "integer": false,
        "lowercase": false,
        "uppercase": false,
        "exported": false
      },
      {
        "name": "integers_associative_array",
        "value": {
          "one": "1",
          "two": "500",
          "three": "999"
        },
        "type": "associative",
        "readonly": false,
        "integer": true,
        "lowercase": false,
        "uppercase": false,
        "exported": false
      }
    ]
"""
import shlex
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`typeset` and `declare` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command']


__version__ = info.version

VAR_DEF_PATTERN = re.compile(r'(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)=(?P<val>[^(][^[].+)$')
SIMPLE_ARRAY_DEF_PATTERN = re.compile(r'(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)=(?P<body>\(\[\d+\]=.+\))$')
ASSOCIATIVE_ARRAY_DEF_PATTERN = re.compile(r'(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)=(?P<body>\(\[[a-zA-Z_][a-zA-Z0-9_]*\]=.+\))$')
EMPTY_ARRAY_DEF_PATTERN = re.compile(r'(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)=\(\)$')
EMPTY_VAR_DEF_PATTERN = re.compile(r'declare\s.+\s(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)$')
DECLARE_OPTS_PATTERN = re.compile(r'declare\s(?P<options>.+?)\s[a-zA-Z_][a-zA-Z0-9_]*')


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for item in proc_data:
        if item['type'] == 'variable' and item['integer']:
            item['value'] = jc.utils.convert_to_int(item['value'])

        elif item['type'] == 'array' and item['integer'] \
            and isinstance(item['value'], list):

            new_num_list = []
            for number in item['value']:
                new_num_list.append(jc.utils.convert_to_int(number))

            item['value'] = new_num_list

        elif (item['type'] == 'array' and item['integer'] \
            and isinstance(item['value'], dict)) \
            or (item['type'] == 'associative' and item['integer']):

            new_num_dict: Dict[str, int] = {}
            for key, val in item['value'].items():
                new_num_dict.update({key: jc.utils.convert_to_int(val)})

            item['value'] = new_num_dict

    return proc_data


def _get_simple_array_vals(body: str) -> List[str]:
    body = _remove_bookends(body)
    body_split = shlex.split(body)
    values = []
    for item in body_split:
        _, val = item.split('=', maxsplit=1)
        values.append(_remove_quotes(val))
    return values


def _get_associative_array_vals(body: str) -> Dict[str, str]:
    body = _remove_bookends(body)
    body_split = shlex.split(body)
    values: Dict = {}
    for item in body_split:
        key, val = item.split('=', maxsplit=1)
        key = _remove_bookends(key, '[', ']')
        values.update({key: val})
    return values


def _get_declare_options(line: str, type_hint: str = 'variable') -> Dict:
    opts = {
        'type': type_hint,
        'readonly': None,
        'integer':  None,
        'lowercase': None,
        'uppercase': None,
        'exported': None
    }

    opts_map = {
        'r': 'readonly',
        'i': 'integer',
        'l': 'lowercase',
        'u': 'uppercase',
        'x': 'exported'
    }

    declare_opts_match = re.match(DECLARE_OPTS_PATTERN, line)
    if declare_opts_match:
        for opt in declare_opts_match['options']:
            if opt in opts_map:
                opts[opts_map[opt]] = True
                continue
        if 'a' in declare_opts_match['options']:
            opts['type'] = 'array'
        elif 'A' in declare_opts_match['options']:
            opts['type'] = 'associative'

        # flip all remaining Nones to False
        for option in opts.items():
            key, val = option
            if val is None:
                opts[key] = False
    return opts


def _remove_bookends(data: str, start_char: str = '(', end_char: str = ')') -> str:
    if data.startswith(start_char) and data.endswith(end_char):
        return data[1:-1]
    return data


def _remove_quotes(data: str, remove_char: str ='"') -> str:
    if data.startswith(remove_char) and data.endswith(remove_char):
        return data[1:-1]
    return data


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

    raw_output: List[Dict] = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            item = {
                "name": '',
                "value": '',
                "type": None,
                "readonly": None,
                "integer":  None,
                "lowercase": None,
                "uppercase": None,
                "exported": None
            }

            # regular variable
            var_def_match = re.search(VAR_DEF_PATTERN, line)
            if var_def_match:
                item['name'] = var_def_match['name']
                item['value'] = _remove_quotes(var_def_match['val'])
                item.update(_get_declare_options(line, 'variable'))
                raw_output.append(item)
                continue

            # empty variable
            empty_var_def_match = re.search(EMPTY_VAR_DEF_PATTERN, line)
            if empty_var_def_match:
                item['name'] = empty_var_def_match['name']
                item['value'] = None
                item.update(_get_declare_options(line, 'variable'))
                raw_output.append(item)
                continue

            # simple array
            simple_arr_def_match = re.search(SIMPLE_ARRAY_DEF_PATTERN, line)
            if simple_arr_def_match:
                item['name'] = simple_arr_def_match['name']
                item['value'] = _get_simple_array_vals(simple_arr_def_match['body'])
                item.update(_get_declare_options(line, 'array'))
                raw_output.append(item)
                continue

            # associative array
            associative_arr_def_match = re.search(ASSOCIATIVE_ARRAY_DEF_PATTERN, line)
            if associative_arr_def_match:
                item['name'] = associative_arr_def_match['name']
                item['value'] = _get_associative_array_vals(associative_arr_def_match['body'])
                item.update(_get_declare_options(line, 'associative'))
                raw_output.append(item)
                continue

            # empty array
            empty_arr_def_match = re.search(EMPTY_ARRAY_DEF_PATTERN, line)
            if empty_arr_def_match:
                item['name'] = empty_arr_def_match['name']
                item['value'] = []
                item.update(_get_declare_options(line, 'array'))
                raw_output.append(item)
                continue

    return raw_output if raw else _process(raw_output)
