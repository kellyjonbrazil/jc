[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc"></a>

# jc.parsers.proc

jc - JSON Convert Proc file output parser

This parser automatically identifies the Proc file and calls the
corresponding parser to perform the parsing.

Magic syntax for converting `/proc` files is also supported by running
`jc /proc/<path to file>`. Any `jc` options must be specified before the
`/proc` path. The magic syntax supports "slurping" multiple files as input.
When multiple files are selected (e.g. `jc /proc/*/stat`) all of the output
will be wrapped inside an array. Also, a `_file` field will be included in
the output which helps correlate the input and output. The `--meta-out`
option can also be used to list the `/proc` input files for correlation with
the output list.

Specific Proc file parsers can also be called directly, if desired, and have
a naming convention of `proc-<name>` (cli) or `proc_<name>` (module). To see
a list of Proc file parsers, use `jc -hh` or `jc -a`.

Usage (cli):

    $ cat /proc/meminfo | jc --proc

or

    $ jc /proc/meminfo

or

    $ cat /proc/meminfo | jc --proc-meminfo

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
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> Union[List[Dict], Dict]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary or List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc.py)

This parser can be used with the `--slurp` command-line option.

Version 1.4 by Kelly Brazil (kellyjonbrazil@gmail.com)
