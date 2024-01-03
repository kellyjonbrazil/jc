[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.jwt"></a>

# jc.parsers.jwt

jc - JSON Convert JWT string parser

> Note: `jc` will not check the integrity of the JWT payload.

Usage (cli):

    $ echo "eyJhbGciOiJIUzI1N..." | jc --jwt

Usage (module):

    import jc
    result = jc.parse('jwt', jwt_string)

Schema:

    {
      "header": {
        "alg":                    string,
        "typ":                    string
      },
      "payload": {
        <key name>:               string/integer/float/boolean/null
      },
      "signature":                string  # [0]
    }

    [0] in colon-delimited hex notation

Examples:

    % echo 'eyJhbGciOiJIUzI1N...' | jc --jwt -p
    {
      "header": {
        "alg": "HS256",
        "typ": "JWT"
      },
      "payload": {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1516239022
      },
      "signature": "49:f9:4a:c7:04:49:48:c7:8a:28:5d:90:4f:87:f0:a4:c7..."
    }

<a id="jc.parsers.jwt.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/jwt.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/jwt.py)

This parser can be used with the `--slurp` command-line option.

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
