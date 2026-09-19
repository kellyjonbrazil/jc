r"""jc - JSON Convert `typeset` and `declare` command output parser

Convert `typeset` and `declare` output from `bash`, `ksh`, and `zsh` with no
options or the following:  `-a`, `-A`, `-i`, `-l`, `-p`, `-r`, `-u`, and `-x`

This parser will serialize ANSI-C quoting in values (e.g. `$'foo'`). Use the
`--raw` option if you don't want quoted values decoded. For example, standard
output of `$'\t\n'` will be `"\t\n"` in JSON. With the `--raw`option it will
output as `"\\t\\n"`.

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

    $ typeset -p | jc --typeset -p    # ksh/zsh
    [
      {
        "name": "user_roles",
        "value": {
          "admin": "alice",
          "guest": "charlie",
          "manager": "bob"
        },
        "type": "associative",
        "readonly": false,
        "integer": false,
        "lowercase": false,
        "uppercase": false,
        "exported": false
      },
      {
        "name": "indexed_array",
        "value": [
          "one",
          "two",
          "three four"
        ],
        "type": "array",
        "readonly": false,
        "integer": false,
        "lowercase": false,
        "uppercase": false,
        "exported": false
      }
    ]
"""
import shlex
import re
from typing import List, Dict, Optional
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`typeset` and `declare` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command']


__version__ = info.version

VAR_DEF_PATTERN = re.compile(r'(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)=(?P<val>[^(].*)$')
SIMPLE_ARRAY_DEF_PATTERN = re.compile(r'(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)=(?P<body>\(\[\d+\]=.+\))$')
# ksh/zsh print indexed arrays as bare values with no [index]= prefix
BARE_ARRAY_DEF_PATTERN = re.compile(r'(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)=(?P<body>\(\s*[^[].*\))$')
# allow a leading space after the paren (zsh) and quoted keys
ASSOCIATIVE_ARRAY_DEF_PATTERN = re.compile(r'(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)=(?P<body>\(\s*\[.+\]=.+\))$')
EMPTY_ARRAY_DEF_PATTERN = re.compile(r'(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)=\(\s*\)$')
EMPTY_VAR_DEF_PATTERN = re.compile(r'(?:declare|typeset)\s.+\s(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)$')

_raw = False

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


def _remove_ansi_c(line):
    pattern = r"\$'((?:[^'\\]|\\.)*)'"

    def decode_ansi_c(match):
        inner_content = match.group(1)

        if _raw:   # global variable because of laziness
            decoded = inner_content
        else:
            decoded = inner_content.encode('utf-8').decode('unicode_escape')

        return f"'{decoded}'"

    return re.sub(pattern, decode_ansi_c, line)


def _get_simple_array_vals(body: str) -> List[str]:
    body = _remove_ansi_c(body)
    body = _remove_bookends(body)
    body_split = shlex.split(body)
    values = []
    for item in body_split:
        _, val = item.split('=', maxsplit=1)
        values.append(_remove_quotes(val))
    return values


def _get_associative_array_vals(body: str) -> Dict[str, str]:
    body = _remove_ansi_c(body)
    body = _remove_bookends(body)
    body_split = shlex.split(body)
    values: Dict = {}
    for item in body_split:
        key, val = item.split('=', maxsplit=1)
        key = _remove_bookends(key, '[', ']')
        values.update({key: val})
    return values


def _get_bare_array_vals(body: str) -> List[str]:
    # ksh/zsh indexed arrays are printed as bare values with no [index]=
    body = _remove_ansi_c(body)
    body = _remove_bookends(body)
    return shlex.split(body)


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

    tokens = line.split()
    keyword = tokens[0] if tokens else ''

    # Bash without `-p` and ksh both print bare `name=value` lines with no
    # keyword. There are no attributes to read, so leave them null like the
    # existing Bash plain-output behavior.
    if keyword not in ('declare', 'typeset', 'export'):
        return opts

    # zsh prints exported scalars with the `export` keyword instead of typeset
    if keyword == 'export':
        opts['exported'] = True

    # gather leading flag tokens; ksh may split them (e.g. `typeset -A -i`)
    flags = ''
    for tok in tokens[1:]:
        if tok.startswith('-'):
            flags += tok
        else:
            break

    for char in flags:
        if char in opts_map:
            opts[opts_map[char]] = True

    if 'a' in flags:
        opts['type'] = 'array'
    elif 'A' in flags:
        opts['type'] = 'associative'

    # flip all remaining Nones to False
    for key, val in opts.items():
        if val is None:
            opts[key] = False

    return opts


def _remove_bookends(data: str, start_char: str = '(', end_char: str = ')') -> str:
    if data.startswith(start_char) and data.endswith(end_char):
        return data[1:-1]
    return data


def _remove_quotes(data: str, remove_char: Optional[str] = None) -> str:
    # strip a matching pair of double or single quotes (ksh/zsh use single quotes)
    if remove_char is None:
        if len(data) >= 2 and data[0] == data[-1] and data[0] in ('"', "'"):
            return data[1:-1]
        return data
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

    global _raw
    _raw = raw

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

            # bare-value indexed array (ksh/zsh have no [index]= prefix)
            bare_arr_def_match = re.search(BARE_ARRAY_DEF_PATTERN, line)
            if bare_arr_def_match:
                item['name'] = bare_arr_def_match['name']
                item['value'] = _get_bare_array_vals(bare_arr_def_match['body'])
                item.update(_get_declare_options(line, 'array'))
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

            # regular variable
            var_def_match = re.search(VAR_DEF_PATTERN, line)
            if var_def_match:
                item['name'] = var_def_match['name']
                item['value'] = _remove_ansi_c(var_def_match['val'])
                item['value'] = _remove_quotes(item['value'])
                item.update(_get_declare_options(line, 'variable'))
                raw_output.append(item)
                continue

    return raw_output if raw else _process(raw_output)
