[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.url"></a>

# jc.parsers.url

jc - JSON Convert URL string parser

This parser will work with naked and wrapped URL strings:

- `scheme://host/path`
- `URL:scheme://host/path`
- `<scheme://host/path>`
- `<URL:scheme://host/path>`

Normalized quoted and unquoted versions of the original URL and URL parts
are included in the output.

Usage (cli):

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url

Usage (module):

    import jc
    result = jc.parse('url', url_string)

Schema:

    {
      "url":                       string,
      'url_encoded":               string,
      "scheme":                    string,
      "scheme_encoded":            string,
      "netloc":                    string,
      "netloc_encoded":            string,
      "path":                      string or null,
      "path_encoded":              string or null,
      "path_list": [               array or null
                                   string
      ],
      "query":                     string or Null,
      "query_encoded":             string or Null,
      "query_obj": {               object or null
        <query-key>: [             array or null
          <query-value>            string             # [0]
        ]
      },
      "fragment":                  string or null,
      "fragment_encoded":          string or null,
      "username":                  string or null,
      "username_encoded":          string or null,
      "password":                  string or null,
      "password_encoded":          string or null,
      "hostname":                  string or null,
      "hostname_encoded":          string or null,
      "port":                      integer or null,
      "port_encoded":              string or null
    }

    [0] Duplicate query-keys will have their values consolidated into the
        array of query-values

Examples:

    % echo "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag" \\
           | jc --url -p
    {
      "url": "http://example.com/test/path?q1=foo&q1=bar&q2=baz#frag",
      "url_encoded": "http://example.com/test/path?q1%3Dfoo%26q1%3Dbar%26q2%3Dbaz#frag",
      "scheme": "http",
      "scheme_encoded": "http",
      "netloc": "example.com",
      "netloc_encoded": "example.com",
      "path": "/test/path",
      "path_encoded": "/test/path",
      "path_list": [
        "test",
        "path"
      ],
      "query": "q1=foo&q1=bar&q2=baz",
      "query_encoded": "q1%3Dfoo%26q1%3Dbar%26q2%3Dbaz",
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
      "fragment_encoded": "frag",
      "username": null,
      "username_encoded": null,
      "password": null,
      "password_encoded": null,
      "hostname": "example.com",
      "hostname_encoded": "example.com",
      "port": null,
      "port_encoded": null
    }

    $ echo "ftp://localhost/filepath" | jc --url -p
    {
      "url": "ftp://localhost/filepath",
      "url_encoded": "ftp://localhost/filepath",
      "scheme": "ftp",
      "scheme_encoded": "ftp",
      "netloc": "localhost",
      "netloc_encoded": "localhost",
      "path": "/filepath",
      "path_encoded": "/filepath",
      "path_list": [
        "filepath"
      ],
      "query": null,
      "query_encoded": null,
      "query_obj": null,
      "fragment": null,
      "fragment_encoded": null,
      "username": null,
      "username_encoded": null,
      "password": null,
      "password_encoded": null,
      "hostname": "localhost",
      "hostname_encoded": "localhost",
      "port": null,
      "port_encoded": null
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
