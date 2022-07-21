[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.url"></a>

# jc.parsers.url

jc - JSON Convert URL string parser

This parser will work with naked and wrapped URL strings:

- `scheme://host/path`
- `URL:scheme://host/path`
- `<scheme://host/path>`
- `<URL:scheme://host/path>`

Two query representations are available and documented in the schema.

Normalized quoted and unquoted versions of the original URL are also
included.

Usage (cli):

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url

Usage (module):

    import jc
    result = jc.parse('url', url_string)

Schema:

    {
      "quoted":               string,
      'unquoted":             string,
      "scheme":               string,
      "netloc":               string,
      "path":                 string or null,
      "path_list": [          array or null
                              string
      ],
      "query": {              object or null
        <query-key>: [        array or null
          <query-value>       string             # [0]
        ]
      },
      "query_list": [         array or null
        [
          <query-key>         string,            # [1]
          <query-value>       string
        ]
      ],
      "fragment":             string or null,
      "username":             string or null,
      "password":             string or null,
      "hostname":             string or null,
      "port":                 integer or null
    }

    [0] Duplicate query-keys will have their values consolidated into the
        array of query-values
    [1] The first array value is the query-key and the second value is the
        query-value

Examples:

    % echo "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag" \\
           | jc --url -p
    {
      "quoted": "http://example.com/test/path?q1%3Dfoo%26q1%3Dbar%26q2%3Dbaz#frag",
      "unquoted": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
      "scheme": "http",
      "netloc": "example.com",
      "path": "/test/path",
      "path_list": [
        "test",
        "path"
      ],
      "query": {
        "q1": [
          "foo",
          "bar"
        ],
        "q2": [
          "baz"
        ]
      },
      "query_list": [
        [
          "q1",
          "foo"
        ],
        [
          "q1",
          "bar"
        ],
        [
          "q2",
          "baz"
        ]
      ],
      "fragment": "frag",
      "username": null,
      "password": null,
      "hostname": "example.com",
      "port": null
    }

    $ echo "ftp://localhost/filepath" | jc --url -p
    {
      "quoted": "ftp://localhost/filepath",
      "unquoted": "ftp://localhost/filepath",
      "scheme": "ftp",
      "netloc": "localhost",
      "path": "/filepath",
      "path_list": [
        "filepath"
      ],
      "query": null,
      "query_list": null,
      "fragment": null,
      "username": null,
      "password": null,
      "hostname": "localhost",
      "port": null
    }

<a id="jc.parsers.url.parse"></a>

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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
