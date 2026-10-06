[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.typeset"></a>

# jc.parsers.typeset

jc - JSON Convert `typeset` and `declare` command output parser

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

<a id="jc.parsers.typeset.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/typeset.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/typeset.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
