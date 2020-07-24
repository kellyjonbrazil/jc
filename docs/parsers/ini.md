# jc.parsers.ini
jc - JSON CLI output utility INI Parser

Usage:

    Specify --ini as the first argument if the piped input is coming from an INI file or any
    simple key/value pair file. Delimiter can be '=' or ':'. Missing values are supported.
    Comment prefix can be '#' or ';'. Comments must be on their own line.

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ cat example.ini
    [DEFAULT]
    ServerAliveInterval = 45
    Compression = yes
    CompressionLevel = 9
    ForwardX11 = yes

    [bitbucket.org]
    User = hg

    [topsecret.server.com]
    Port = 50022
    ForwardX11 = no

    $ cat example.ini | jc --ini -p
    {
      "bitbucket.org": {
        "serveraliveinterval": "45",
        "compression": "yes",
        "compressionlevel": "9",
        "forwardx11": "yes",
        "user": "hg"
      },
      "topsecret.server.com": {
        "serveraliveinterval": "45",
        "compression": "yes",
        "compressionlevel": "9",
        "forwardx11": "no",
        "port": "50022"
      }
    }

## info
```python
info(self, /, *args, **kwargs)
```

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    Dictionary representing an ini document:

    {
      ini or key/value document converted to a dictionary - see configparser standard
      library documentation for more details.

      Note: Values starting and ending with quotation marks will have the marks removed.
            If you would like to keep the quotation markes, use the -r or raw=True argument.
    }

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary representing the ini file

