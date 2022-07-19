[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.url"></a>

# jc.parsers.url

jc - JSON Convert URL string parser

Usage (cli):

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url

Usage (module):

    import jc
    result = jc.parse('url', url_string)

Schema:

    {
      "scheme":               string,
      "netloc":               string,
      "path":                 string or null,
      "query": {              object or null,
        <query-key>:          string
      },
      "fragment":             string or null,
      "username":             string or null,
      "password":             string or null,
      "hostname":             string or null,
      "port":                 integer or null
    }

Examples:

    $ echo "http://example.com/test/path?q1=foo&q2=bar#frag" | jc --url -p
    {
      "scheme": "http",
      "netloc": "example.com",
      "path": "/test/path",
      "query": {
        "q1": "foo",
        "q2": "bar"
      },
      "fragment": "frag",
      "username": null,
      "password": null,
      "hostname": "example.com",
      "port": null
    }

    $ echo "ftp://localhost/filepath" | jc --url -p
    {
      "scheme": "ftp",
      "netloc": "localhost",
      "path": "/filepath",
      "query": null,
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
