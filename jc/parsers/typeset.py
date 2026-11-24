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
    version = '1.2'
    description = '`typeset` and `declare` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command']


__version__ = info.version

# The variable name is the word directly before the first `=` on the line, so
# each pattern is tried once per line rather than at every offset of the value.
NAME_PATTERN = r'^[^=]*(?<![a-zA-Z0-9_])(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)='
# array definitions end the line with `)`; check that before matching the body
ARRAY_NAME_PATTERN = NAME_PATTERN + r'(?=\(.*\)$)'
VAR_DEF_PATTERN = re.compile(NAME_PATTERN + r'(?P<val>[^(].*)$')
SIMPLE_ARRAY_DEF_PATTERN = re.compile(ARRAY_NAME_PATTERN + r'(?P<body>\(\[\d+\]=.+\))$')
# ksh/zsh print indexed arrays as bare values with no [index]= prefix
BARE_ARRAY_DEF_PATTERN = re.compile(ARRAY_NAME_PATTERN + r'(?P<body>\(\s*[^[].*\))$')
# allow a leading space after the paren (zsh) and quoted keys
ASSOCIATIVE_ARRAY_DEF_PATTERN = re.compile(ARRAY_NAME_PATTERN + r'(?P<body>\(\s*\[.+\]=.+\))$')
EMPTY_ARRAY_DEF_PATTERN = re.compile(ARRAY_NAME_PATTERN + r'\(\s*\)$')
EMPTY_VAR_DEF_PATTERN = re.compile(r'^\s*(?:declare|typeset)\s.+\s(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)$')

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


_ANSI_C_PATTERN = re.compile(r"\$'((?:[^'\\]|\\.)*)'")

# For array bodies: backslash escapes and ordinary "..." and '...' strings are
# matched first and kept as they are, so only a `$'` that starts a word is
# taken as ANSI-C quoting.
_ARRAY_ANSI_C_PATTERN = re.compile(r"""\\.|"(?:[^"\\]|\\.)*"|'[^']*'|\$'((?:[^'\\]|\\.)*)'""")


def _remove_ansi_c(line, shell_quote=False):
    def decode_ansi_c(match):
        inner_content = match.group(1)

        if inner_content is None:
            return match.group(0)

        if _raw:   # global variable because of laziness
            decoded = inner_content
        else:
            decoded = inner_content.encode('utf-8').decode('unicode_escape')

        if shell_quote:
            # array bodies are split with _shell_split() afterwards, so quote
            # the text to keep it one word
            return shlex.quote(decoded)

        return f"'{decoded}'"

    if shell_quote:
        return _ARRAY_ANSI_C_PATTERN.sub(decode_ansi_c, line)

    return _ANSI_C_PATTERN.sub(decode_ansi_c, line)


# a word: runs of plain characters, quoted strings and escaped characters
_SHELL_WORD = re.compile(r'''(?:[^ \t\r\n'"\\]+|'[^']*'|"(?:[^"\\]|\\.)*"|\\.)+''', re.DOTALL)
_SHELL_PART = re.compile(r'''[^'"\\]+|'([^']*)'|"((?:[^"\\]|\\.)*)"|\\(.)''', re.DOTALL)
_DQ_ESCAPE = re.compile(r'\\([\\"])')
_DQ_TAIL = re.compile(r'(?:[^"\\]|\\.)*\\', re.DOTALL)


def _shell_words(data):
    """Split like shlex.split() (POSIX mode, no comments), keeping the quotes"""
    words = []
    pos = 0
    end = len(data)
    while True:
        while pos < end and data[pos] in ' \t\r\n':
            pos += 1
        if pos >= end:
            return words
        match = _SHELL_WORD.match(data, pos)
        stop = match.end() if match else pos
        if stop < end and data[stop] not in ' \t\r\n':
            # the same errors as shlex: the input ends after a backslash
            # (outside of single quotes) or inside quotes
            if data[stop] == '\\' or (data[stop] == '"' and _DQ_TAIL.fullmatch(data, stop + 1)):
                raise ValueError('No escaped character')
            raise ValueError('No closing quotation')
        words.append(data[pos:stop])
        pos = stop


def _shell_unquote(word):
    """Remove the quotes and escapes from a word of _shell_words()"""
    result = []
    for part in _SHELL_PART.finditer(word):
        single, double, escaped = part.groups()
        if single is not None:
            result.append(single)
        elif double is not None:
            result.append(_DQ_ESCAPE.sub(r'\1', double))
        elif escaped is not None:
            result.append(escaped)
        else:
            result.append(part.group(0))
    return ''.join(result)


def _shell_split(data):
    """
    Same result as shlex.split(data), which takes quadratic time on a long
    word
    """
    return [_shell_unquote(word) for word in _shell_words(data)]


def _get_simple_array_vals(body: str) -> List[str]:
    body = _remove_ansi_c(body, shell_quote=True)
    body = _remove_bookends(body)
    body_split = _shell_split(body)
    values = []
    for item in body_split:
        _, val = item.split('=', maxsplit=1)
        values.append(_remove_quotes(val))
    return values


def _split_key_value(word: str):
    """
    Split a `[key]=value` word at the first `]=` outside of quotes, so a key
    can contain `=`. Returns None if there is no such `]=`.
    """
    if not word.startswith('['):
        return None

    for part in _SHELL_PART.finditer(word, 1):
        if part.group(0)[0] not in '\'"\\':
            idx = part.group(0).find(']=')
            if idx != -1:
                idx += part.start()
                return _shell_unquote(word[1:idx]), _shell_unquote(word[idx + 2:])

    return None


def _get_associative_array_vals(body: str) -> Dict[str, str]:
    body = _remove_ansi_c(body, shell_quote=True)
    body = _remove_bookends(body)
    values: Dict = {}
    for word in _shell_words(body):
        key_value = _split_key_value(word)
        if key_value:
            key, val = key_value
        else:
            key, val = _shell_unquote(word).split('=', maxsplit=1)
            key = _remove_bookends(key, '[', ']')
        values.update({key: val})
    return values


def _get_bare_array_vals(body: str) -> List[str]:
    # ksh/zsh indexed arrays are printed as bare values with no [index]=
    body = _remove_ansi_c(body, shell_quote=True)
    body = _remove_bookends(body)
    return _shell_split(body)


def _get_flags(line: str) -> str:
    """Return the leading option flags of a declare/typeset/export line."""
    tokens = line.split()
    if not tokens or tokens[0] not in ('declare', 'typeset', 'export'):
        return ''

    # gather leading flag tokens; ksh may split them (e.g. `typeset -A -i`)
    flags = ''
    for tok in tokens[1:]:
        if tok.startswith('-'):
            flags += tok
        else:
            break

    return flags


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

    flags = _get_flags(line)

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

        for line in filter(None, jc.utils.splitlines(data)):

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

            # simple array. A line declared with -A is an associative array
            # even when its first key is a number.
            flags = _get_flags(line)
            is_assoc = 'A' in flags and 'a' not in flags
            simple_arr_def_match = None if is_assoc else re.search(SIMPLE_ARRAY_DEF_PATTERN, line)
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
