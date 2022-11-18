[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc"></a>

# jc.parsers.proc

jc - JSON Convert Proc file output parser

This parser automatically identifies the Proc file and calls the
corresponding parser to perform the parsing.

Magic syntax for converting `/proc` files is also supported by running
`jc /proc/<path to file>`. Any `jc` options must be specified before the
`/proc` path.

specific Proc file parsers can also be called directly, if desired and have
a naming convention of `proc-<name>` (cli) or `proc_<name>` (module).

Usage (cli):

    $ cat /proc/meminfo | jc --proc

or

    $ jc /proc/meminfo

or

    $ cat /proc/meminfo | jc --proc-memifno

Usage (module):

    import jc
    result = jc.parse('proc', proc_file)

Schema:

See the specific Proc parser for the schema:

    $ jc --help --proc-<name>

For example:

    $ jc --help --proc-meminfo

Specific Proc file parser names can be found with `jc -hh` or `jc -a`.

Schemas can also be found online at:

    https://kellyjonbrazil.github.io/jc/docs/parsers/proc_<name>

For example:

    https://kellyjonbrazil.github.io/jc/docs/parsers/proc_meminfo

Examples:

    $ cat /proc/modules | jc --proc -p
    [
      {
        "module": "binfmt_misc",
        "size": 24576,
        "used": 1,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0ab4000"
      },
      {
        "module": "vsock_loopback",
        "size": 16384,
        "used": 0,
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0a14000"
      },
      {
        "module": "vmw_vsock_virtio_transport_common",
        "size": 36864,
        "used": 1,
        "used_by": [
          "vsock_loopback"
        ],
        "status": "Live",
        "location": "0xffffffffc0a03000"
      },
      ...
    ]

    $ cat /proc/modules | jc --proc-modules -p -r
    [
      {
        "module": "binfmt_misc",
        "size": "24576",
        "used": "1",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0ab4000"
      },
      {
        "module": "vsock_loopback",
        "size": "16384",
        "used": "0",
        "used_by": [],
        "status": "Live",
        "location": "0xffffffffc0a14000"
      },
      {
        "module": "vmw_vsock_virtio_transport_common",
        "size": "36864",
        "used": "1",
        "used_by": [
          "vsock_loopback"
        ],
        "status": "Live",
        "location": "0xffffffffc0a03000"
      },
      ...
    ]

<a id="jc.parsers.proc.parse"></a>

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

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
