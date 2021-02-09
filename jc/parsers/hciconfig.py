"""jc - JSON CLI output utility `hciconfig` command output parser

<<Short hciconfig description and caveats>>

Usage (cli):

    $ hciconfig | jc --hciconfig

    or

    $ jc hciconfig

Usage (module):

    import jc.parsers.hciconfig
    result = jc.parsers.hciconfig.parse(hciconfig_command_output)

Compatibility:

    'linux'

Examples:

    $ hciconfig | jc --hciconfig -p
    []

    $ hciconfig | jc --hciconfig -p -r
    []
"""
import jc.utils


class info():
    version = '1.0'
    description = 'hciconfig command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['hciconfig']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data with the following schema:

        [
          {
            "device":               string,
            "type":                 string,
            "bus":                  string,
            "bd_address":           string,
            "acl_mtu":              integer,
            "acl_mtu_packets":      integer,
            "sco_mtu":              integer,
            "sco_mtu_packets":      integer,
            "state": [
                                    string
            ],
            "rx_bytes":             integer,
            "rx_acl":               integer,
            "rx_sco":               integer,
            "rx_events":            integer,
            "rx_errors":            integer,
            "tx_bytes":             integer,
            "tx_acl":               integer,
            "tx_sco":               integer,
            "tx_commands":          integer,
            "tx_errors":            integer,
            "features": [
                                    string
            ],
            "packet_type": [
                                    string
            ],
            "link_policy": [
                                    string
            ],
            "link_mode": [
                                    string
            ],
            "name":                 string,
            "class":                string,
            "service_classes": [
                                    string
            ],
            "device_class":         string,
            "hci_version":          string,
            "revision":             string,
            "lmp_version":          string,
            "subversion":           string,
            "manufacturer":         string
          }
        ]
    """

    # rebuild output for added semantic information
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

    raw_output = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            # parse the content
            pass

    if raw:
        return raw_output
    else:
        return process(raw_output)
