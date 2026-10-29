r"""jc - JSON Convert `/etc/hosts` file parser

Usage (cli):

    $ cat /etc/hosts | jc --hosts

Usage (module):

    import jc
    result = jc.parse('hosts', hosts_file_output)

Schema:

    [
      {
        "ip":           string,
        "hostname": [
                        string
        ]
      }
    ]

Examples:

    $ cat /etc/hosts | jc --hosts -p
    [
      {
        "ip": "127.0.0.1",
        "hostname": [
          "localhost"
        ]
      },
      {
        "ip": "127.0.1.1",
        "hostname": [
          "root-ubuntu"
        ]
      },
      {
        "ip": "::1",
        "hostname": [
          "ip6-localhost",
          "ip6-loopback"
        ]
      },
      {
        "ip": "fe00::0",
        "hostname": [
          "ip6-localnet"
        ]
      },
      {
        "ip": "ff00::0",
        "hostname": [
          "ip6-mcastprefix"
        ]
      },
      {
        "ip": "ff02::1",
        "hostname": [
          "ip6-allnodes"
        ]
      },
      {
        "ip": "ff02::2",
        "hostname": [
          "ip6-allrouters"
        ]
      }
    ]
"""
import re
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.6'
    description = '`/etc/hosts` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """

    # no additional processing needed
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []

    # Clear any blank lines
    cleandata = [line for line in jc.utils.splitlines(data, split_cr=True) if line.strip()]

    if jc.utils.has_data(data):

        for line in cleandata:
            output_line = {}
            # ignore commented lines
            if line.strip().startswith('#'):
                continue

            # a comment starts at the first '#', even in the middle of a word
            line = line.split('#', 1)[0]
            line_list = re.findall(r'\S+', line, flags=re.ASCII)
            if not line_list:
                continue

            ip = line_list[0]
            hosts_list = line_list[1:]

            output_line['ip'] = ip
            output_line['hostname'] = hosts_list

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
