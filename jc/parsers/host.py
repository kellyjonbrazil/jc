r"""jc - JSON Convert `host` command output parser

Supports parsing of the most commonly used RR types (A, AAAA, MX, TXT)

Usage (cli):

    $ host google.com | jc --host

or

    $ jc host google.com

Usage (module):

    import jc
    result = jc.parse('host', host_command_output)

Schema:

    [
      {
        "hostname":     string,
        "address": [
                        string
        ],
        "v6-address": [
                        string
        ],
        "mail": [
                        string
        ]
      }
    ]

    [
      {
        "nameserver":   string,
        "zone":         string,
        "mname":        string,
        "rname":        string,
        "serial":       integer,
        "refresh":      integer,
        "retry":        integer,
        "expire":       integer,
        "minimum":      integer
      }
    ]

Examples:

    $ host google.com | jc --host
    [
      {
        "hostname": "google.com",
        "address": [
          "142.251.39.110"
        ],
        "v6-address": [
          "2a00:1450:400e:811::200e"
        ],
        "mail": [
          "smtp.google.com."
        ]
      }
    ]

    $ jc host -C sunet.se
    [
      {
        "nameserver": "2001:6b0:7::2",
        "zone": "sunet.se",
        "mname": "sunic.sunet.se.",
        "rname": "hostmaster.sunet.se.",
        "serial": "2023090401",
        "refresh": "28800",
        "retry": "7200",
        "expire": "604800",
        "minimum": "300"
      },
      {
        ...
      }
    ]
"""
from typing import Dict, List
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`host` command parser'
    author = 'Pettai'
    author_email = 'pettai@sunet.se'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command']
    magic_commands = ['host']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    int_list = {'serial', 'refresh', 'retry', 'expire', 'minimum'}

    for entry in proc_data:
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])

    return proc_data


def parse(data: str, raw: bool = False, quiet: bool = False):
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

    raw_output: List[Dict] = []

    warned = False

    if jc.utils.has_data(data):

        addresses = []
        v6addresses = []
        mail = []
        text = []
        rrdata = {}
        soaparse = False

        for line in filter(None, jc.utils.splitlines(data)):
            line = line.strip()

            # the record type words directly follow the owner name, which
            # has no spaces. The same words can also appear in record data.
            rrtype = line.partition(' ')[2]

            # TXT parsing
            if rrtype.startswith('descriptive text '):
                linedata = line.split(' ', maxsplit=3)
                hostname = linedata[0]
                txt = linedata[3].strip('"')
                text.append(txt)
                rrdata.update({'hostname': hostname})
                rrdata.update({'text': text})
                continue

            # default
            if rrtype.startswith('has address '):
                linedata = line.split(' ', maxsplit=3)
                hostname = linedata[0]
                address = linedata[3]
                addresses.append(address)
                rrdata.update({'hostname': hostname})
                rrdata.update({'address': addresses})
                continue

            if rrtype.startswith('has IPv6 address '):
                linedata = line.split(' ', maxsplit=4)
                hostname = linedata[0]
                v6address = linedata[4]
                v6addresses.append(v6address)
                rrdata.update({'hostname': hostname})
                rrdata.update({'v6-address': v6addresses})
                continue

            if rrtype.startswith('mail is handled by '):
                linedata = line.split(' ', maxsplit=6)
                hostname = linedata[0]
                mx = linedata[6]
                mail.append(mx)
                rrdata.update({'hostname': hostname})
                rrdata.update({'mail': mail})
                continue

            # -C / SOA parsing
            if line.startswith('Nameserver '):
                soaparse = True
                rrdata = {}
                linedata = line.split(' ', maxsplit=1)
                nameserverip = linedata[1]

                # host prints 'Nameserver <address>:'. Remove only that colon,
                # an IPv6 address can end with colons too. (e.g. 2001:db8::)
                if nameserverip.endswith(':'):
                    nameserverip = nameserverip[:-1]

                rrdata.update({'nameserver': nameserverip})
                continue

            if rrtype.startswith('has SOA record '):
                # without -C, a second SOA line is a separate record
                if not soaparse and 'zone' in rrdata:
                    raw_output.append(rrdata)
                    rrdata = {}

                linedata = line.split(' ', maxsplit=10)

                zone = linedata[0]
                mname = linedata[4]
                rname = linedata[5]
                serial = linedata[6]
                refresh = linedata[7]
                retry = linedata[8]
                expire = linedata[9]
                minimum = linedata[10]

                try:
                    rrdata.update(
                        {
                            'zone': zone,
                            'mname': mname,
                            'rname': rname,
                            'serial': serial,
                            'refresh': refresh,
                            'retry': retry,
                            'expire': expire,
                            'minimum': minimum 
                        },
                    )

                    # -C output: each SOA line completes a record, so start a
                    # new one. Otherwise the single record is appended after
                    # the loop.
                    if soaparse:
                        raw_output.append(rrdata)
                        rrdata = {}

                except IndexError:
                    if not warned:
                        jc.utils.warning_message(['Unknown format detected.'])
                        warned = True

        if not soaparse:
            raw_output.append(rrdata)

    return raw_output if raw else _process(raw_output)
