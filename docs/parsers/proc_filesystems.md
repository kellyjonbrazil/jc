[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_filesystems"></a>

# jc.parsers.proc_filesystems

jc - JSON Convert `/proc/filesystems` file parser

Usage (cli):

    $ cat /proc/filesystems | jc --proc

or

    $ jc /proc/filesystems

or

    $ cat /proc/filesystems | jc --proc-filesystems

Usage (module):

    import jc
    result = jc.parse('proc', proc_filesystems_file)

or

    import jc
    result = jc.parse('proc_filesystems', proc_filesystems_file)

Schema:

    [
      {
        "filesystem":               string,
        "nodev":                    boolean
      }
    ]

Examples:

    $ cat /proc/filesystems | jc --proc -p
    [
      {
          "filesystem": "sysfs",
          "nodev": true
      },
      {
          "filesystem": "tmpfs",
          "nodev": true
      },
      {
          "filesystem": "bdev",
          "nodev": true
      },
      ...
    ]

<a id="jc.parsers.proc_filesystems.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc_filesystems.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_filesystems.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
