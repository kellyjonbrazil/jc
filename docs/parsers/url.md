[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.url"></a>

# jc.parsers.url

jc - JSON Convert URL string parser

Normalized, Encoded, and Decoded versions of the original URL and URL parts
are included in the output. Encoding and Decoding is best effort.

> Note: Do not use the Encoded fields for a URL that has already been
> Encoded. Similarly, do not use the Decoded fields for a URL that has
> already been Decoded.

This parser will work with naked and wrapped URL strings:

- `/path`
- `scheme://host/path`
- `URL:scheme://host/path`
- `<scheme://host/path>`
- `<URL:scheme://host/path>`

Usage (cli):

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url

Usage (module):

    import jc
    result = jc.parse('url', url_string)

Schema:

    {
      "url":                       string,
      "scheme":                    string or null,
      "netloc":                    string or null,
      "path":                      string or null,
      "parent":                    string or null,
      "filename":                  string or null,
      "stem":                      string or null,
      "extension":                 string or null,
      "path_list": [               array or null
                                   string
      ],
      "query":                     string or null,
      "query_obj": {               object or null
        <query-key>: [             array or null
          <query-value>            string            # [0]
        ]
      },
      "fragment":                  string or null,
      "username":                  string or null,
      "password":                  string or null,
      "hostname":                  string or null,
      "port":                      integer or null,  # [1]
      "encoded": {
        "url":                     string,
        "scheme":                  string or null,
        "netloc":                  string or null,
        "path":                    string or null,
        "parent":                  string or null,
        "filename":                string or null,
        "stem":                    string or null,
        "extension":               string or null,
        "path_list": [             array or null
                                   string
        ],
        "query":                   string or null,
        "fragment":                string or null,
        "username":                string or null,
        "password":                string or null,
        "hostname":                string or null,
        "port":                    integer or null,  # [1]
      },
      "decoded": {
        "url":                     string,
        "scheme":                  string or null,
        "netloc":                  string or null,
        "path":                    string or null,
        "parent":                  string or null,
        "filename":                string or null,
        "stem":                    string or null,
        "extension":               string or null,
        "path_list": [             array or null
                                   string
        ],
        "query":                   string or null,
        "fragment":                string or null,
        "username":                string or null,
        "password":                string or null,
        "hostname":                string or null,
        "port":                    integer or null,  # [1]
      }
    }

    [0] Duplicate query-keys will have their values consolidated into the
        array of query-values

    [1] Invalid port values will be converted to null/None and a warning
        message will be printed to `STDERR` if quiet=False

Examples:

    $ echo "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag" \\
           | jc --url -p
    {
      "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
      "scheme": "http",
      "netloc": "example.com",
      "path": "/test/path",
      "parent": "/test",
      "filename": "path",
      "stem": "path",
      "extension": null,
      "path_list": [
        "test",
        "path"
      ],
      "query": "q1=foo&q1=bar&q2=baz",
      "query_obj": {
        "q1": [
          "foo",
          "bar"
        ],
        "q2": [
          "baz"
        ]
      },
      "fragment": "frag",
      "username": null,
      "password": null,
      "hostname": "example.com",
      "port": null,
      "encoded": {
        "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
        "scheme": "http",
        "netloc": "example.com",
        "path": "/test/path",
        "parent": "/test",
        "filename": "path",
        "stem": "path",
        "extension": null,
        "path_list": [
          "test",
          "path"
        ],
        "query": "q1=foo&q1=bar&q2=baz",
        "fragment": "frag",
        "username": null,
        "password": null,
        "hostname": "example.com",
        "port": null
      },
      "decoded": {
        "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
        "scheme": "http",
        "netloc": "example.com",
        "path": "/test/path",
        "parent": "/test",
        "filename": "path",
        "stem": "path",
        "extension": null,
        "path_list": [
          "test",
          "path"
        ],
        "query": "q1=foo&q1=bar&q2=baz",
        "fragment": "frag",
        "username": null,
        "password": null,
        "hostname": "example.com",
        "port": null
      }
    }

    $ echo "ftp://localhost/filepath" | jc --url -p
    {
      "url": "ftp://localhost/filepath",
      "scheme": "ftp",
      "netloc": "localhost",
      "path": "/filepath",
      "parent": "/",
      "filename": "filepath",
      "stem": "filepath",
      "extension": null,
      "path_list": [
        "filepath"
      ],
      "query": null,
      "query_obj": null,
      "fragment": null,
      "username": null,
      "password": null,
      "hostname": "localhost",
      "port": null,
      "encoded": {
        "url": "ftp://localhost/filepath",
        "scheme": "ftp",
        "netloc": "localhost",
        "path": "/filepath",
        "parent": "/",
        "filename": "filepath",
        "stem": "filepath",
        "extension": null,
        "path_list": [
          "filepath"
        ],
        "query": null,
        "fragment": null,
        "username": null,
        "password": null,
        "hostname": "localhost",
        "port": null
      },
      "decoded": {
        "url": "ftp://localhost/filepath",
        "scheme": "ftp",
        "netloc": "localhost",
        "path": "/filepath",
        "parent": "/",
        "filename": "filepath",
        "stem": "filepath",
        "extension": null,
        "path_list": [
          "filepath"
        ],
        "query": null,
        "fragment": null,
        "username": null,
        "password": null,
        "hostname": "localhost",
        "port": null
      }
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

Source: [`jc/parsers/url.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/url.py)

This parser can be used with the `--slurp` command-line option.

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
