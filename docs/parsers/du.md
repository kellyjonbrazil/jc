
# jc.parsers.du
jc - JSON CLI output utility `du` command output parser

Usage (cli):

    $ du | jc --du

    or

    $ jc du

Usage (module):

    import jc.parsers.du
    result = jc.parsers.du.parse(du_command_output)

Schema:

    [
      {
        "size":     integer,
        "name":     string
      }
    ]

Compatibility:

    'linux', 'darwin', 'aix', 'freebsd'

Examples:

    $ du /usr | jc --du -p
    [
      {
        "size": 104608,
        "name": "/usr/bin"
      },
      {
        "size": 56,
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/_CodeSignature"
      },
      {
        "size": 0,
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr/local/standalone"
      },
      {
        "size": 0,
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr/local"
      },
      {
        "size": 0,
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr"
      },
      {
        "size": 1008,
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/dfu"
      },
      ...
    ]

    $ du /usr | jc --du -p -r
    [
      {
        "size": "104608",
        "name": "/usr/bin"
      },
      {
        "size": "56",
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/_CodeSignature"
      },
      {
        "size": "0",
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr/local/standalone"
      },
      {
        "size": "0",
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr/local"
      },
      {
        "size": "0",
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/usr"
      },
      {
        "size": "1008",
        "name": "/usr/standalone/firmware/iBridge1_1Customer.bundle/Contents/Resources/Firmware/dfu"
      },
      ...
    ]


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

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

    List of Dictionaries. Raw or processed structured data.

