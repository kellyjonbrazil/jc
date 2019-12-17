# jc.parsers.du
jc - JSON CLI output utility du Parser

Usage:

    specify --du as the first argument if the piped input is coming from du

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

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

    List of dictionaries. Structured data with the following schema:

    [
      {
        "size":     integer,
        "name":     string
      }
    ]

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

    List of dictionaries. Raw or processed structured data.

