# jc.parsers.df
jc - JSON CLI output utility df Parser

Usage:
    specify --df as the first argument if the piped input is coming from df

Examples:

    $ df | jc --df -p
    [
      {
        "filesystem": "devtmpfs",
        "1k-blocks": 1918820,
        "used": 0,
        "available": 1918820,
        "use_percent": 0,
        "mounted_on": "/dev"
      },
      {
        "filesystem": "tmpfs",
        "1k-blocks": 1930668,
        "used": 0,
        "available": 1930668,
        "use_percent": 0,
        "mounted_on": "/dev/shm"
      },
      {
        "filesystem": "tmpfs",
        "1k-blocks": 1930668,
        "used": 11800,
        "available": 1918868,
        "use_percent": 1,
        "mounted_on": "/run"
      },
      ...
    ]

    $ df | jc --df -p -r
    [
      {
        "filesystem": "devtmpfs",
        "1k-blocks": "1918820",
        "used": "0",
        "available": "1918820",
        "use_percent": "0%",
        "mounted_on": "/dev"
      },
      {
        "filesystem": "tmpfs",
        "1k-blocks": "1930668",
        "used": "0",
        "available": "1930668",
        "use_percent": "0%",
        "mounted_on": "/dev/shm"
      },
      {
        "filesystem": "tmpfs",
        "1k-blocks": "1930668",
        "used": "11800",
        "available": "1918868",
        "use_percent": "1%",
        "mounted_on": "/run"
      },
      ...
    ]

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data    (dictionary) raw structured data to process

Returns:

    dictionary   structured data with the following schema:

    [
      {
        "filesystem":   string,
        "size":         string,
        "1k-blocks":    integer,
        "used":         integer,
        "available":    integer,
        "use_percent":  integer,
        "mounted_on":   string
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

    dictionary   raw or processed structured data

