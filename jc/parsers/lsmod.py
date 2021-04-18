"""jc - JSON CLI output utility `lsmod` command output parser

Usage (cli):

    $ lsmod | jc --lsmod

    or

    $ jc lsmod

Usage (module):

    import jc.parsers.lsmod
    result = jc.parsers.lsmod.parse(lsmod_command_output)

Schema:

    [
      {
        "module":     string,
        "size":       integer,
        "used":       integer,
        "by": [
                      string
        ]
      }
    ]

Examples:

    $ lsmod | jc --lsmod -p
    [
      ...
      {
        "module": "nf_nat",
        "size": 26583,
        "used": 3,
        "by": [
          "nf_nat_ipv4",
          "nf_nat_ipv6",
          "nf_nat_masquerade_ipv4"
        ]
      },
      {
        "module": "iptable_mangle",
        "size": 12695,
        "used": 1
      },
      {
        "module": "iptable_security",
        "size": 12705,
        "used": 1
      },
      {
        "module": "iptable_raw",
        "size": 12678,
        "used": 1
      },
      {
        "module": "nf_conntrack",
        "size": 139224,
        "used": 7,
        "by": [
          "nf_nat",
          "nf_nat_ipv4",
          "nf_nat_ipv6",
          "xt_conntrack",
          "nf_nat_masquerade_ipv4",
          "nf_conntrack_ipv4",
          "nf_conntrack_ipv6"
        ]
      },
      ...
    ]

    $ lsmod | jc --lsmod -p -r
    [
      ...
      {
        "module": "nf_conntrack",
        "size": "139224",
        "used": "7",
        "by": [
          "nf_nat",
          "nf_nat_ipv4",
          "nf_nat_ipv6",
          "xt_conntrack",
          "nf_nat_masquerade_ipv4",
          "nf_conntrack_ipv4",
          "nf_conntrack_ipv6"
        ]
      },
      {
        "module": "ip_set",
        "size": "45799",
        "used": "0"
      },
      {
        "module": "nfnetlink",
        "size": "14519",
        "used": "1",
        "by": [
          "ip_set"
        ]
      },
      {
        "module": "ebtable_filter",
        "size": "12827",
        "used": "1"
      },
      {
        "module": "ebtables",
        "size": "35009",
        "used": "2",
        "by": [
          "ebtable_nat",
          "ebtable_filter"
        ]
      },
      ...
    ]
"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = '`lsmod` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['lsmod']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    for entry in proc_data:
        int_list = ['size', 'used']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    cleandata = data.splitlines()
    raw_output = []

    if jc.utils.has_data(data):

        cleandata[0] = cleandata[0].lower()

        raw_output = jc.parsers.universal.simple_table_parse(cleandata)

        for mod in raw_output:
            if 'by' in mod:
                mod['by'] = mod['by'].split(',')

    if raw:
        return raw_output
    else:
        return _process(raw_output)
