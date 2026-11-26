r"""jc - JSON Convert `/proc/net/wireless` file parser

Usage (cli):

    $ cat /proc/net/wireless | jc --proc

or

    $ jc /proc/net/wireless

or

    $ cat /proc/net/wireless | jc --proc-net-wireless

Usage (module):

    import jc
    result = jc.parse('proc', proc_net_wireless_file)

or

    import jc
    result = jc.parse('proc_net_wireless', proc_net_wireless_file)

Schema:

    [
      {
        "interface":                  string,
        "status":                     integer,
        "quality_link":               integer,
        "quality_link_updated":       boolean,
        "quality_level":              integer,
        "quality_level_updated":      boolean,
        "quality_noise":              integer,
        "quality_noise_updated":      boolean,
        "discarded_nwid":             integer,
        "discarded_crypt":            integer,
        "discarded_frag":             integer,
        "discarded_retry":            integer,
        "discarded_misc":             integer,
        "missed_beacon":              integer
      }
    ]

Examples:

    $ cat /proc/net/wireless | jc --proc -p
    [
      {
        "interface": "wlp0s20f3",
        "status": 0,
        "quality_link": 58,
        "quality_link_updated": true,
        "quality_level": -52,
        "quality_level_updated": true,
        "quality_noise": -256,
        "quality_noise_updated": false,
        "discarded_nwid": 0,
        "discarded_crypt": 0,
        "discarded_frag": 0,
        "discarded_retry": 12,
        "discarded_misc": 7,
        "missed_beacon": 0
      },
      {
        "interface": "wlan1",
        "status": 10,
        "quality_link": 70,
        "quality_link_updated": true,
        "quality_level": -40,
        "quality_level_updated": true,
        "quality_noise": -95,
        "quality_noise_updated": true,
        "discarded_nwid": 3,
        "discarded_crypt": 1,
        "discarded_frag": 0,
        "discarded_retry": 1543,
        "discarded_misc": 210,
        "missed_beacon": 18
      }
    ]

    $ cat /proc/net/wireless | jc --proc-net-wireless -p -r
    [
      {
        "interface": "wlp0s20f3",
        "status": "0000",
        "quality_link": "58.",
        "quality_level": "-52.",
        "quality_noise": "-256",
        "discarded_nwid": "0",
        "discarded_crypt": "0",
        "discarded_frag": "0",
        "discarded_retry": "12",
        "discarded_misc": "7",
        "missed_beacon": "0"
      },
      {
        "interface": "wlan1",
        "status": "000a",
        "quality_link": "70.",
        "quality_level": "-40.",
        "quality_noise": "-95.",
        "discarded_nwid": "3",
        "discarded_crypt": "1",
        "discarded_frag": "0",
        "discarded_retry": "1543",
        "discarded_misc": "210",
        "missed_beacon": "18"
      }
    ]
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
from jc.exceptions import ParseError
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/net/wireless` file parser'
    author = 'Michael Klemm'
    author_email = 'MichaelKlemm@users.noreply.github.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


_FIELDS = (
    'status', 'quality_link', 'quality_level', 'quality_noise', 'discarded_nwid',
    'discarded_crypt', 'discarded_frag', 'discarded_retry', 'discarded_misc',
    'missed_beacon'
)
_QUALITY_FIELDS = ('quality_link', 'quality_level', 'quality_noise')


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    processed: List[JSONDictType] = []

    for entry in proc_data:
        item: Dict = {'interface': entry['interface']}

        # the status is printed in hex
        try:
            item['status'] = int(entry['status'], 16)
        except ValueError:
            item['status'] = None

        for key in _FIELDS[1:]:
            # a quality value ends with a dot if it was updated since the
            # last read
            if key in _QUALITY_FIELDS:
                item[key] = jc.utils.convert_to_int(entry[key].rstrip('.'))
                item[key + '_updated'] = entry[key].endswith('.')
            else:
                item[key] = jc.utils.convert_to_int(entry[key])

        processed.append(item)

    return processed


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
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

    if jc.utils.has_data(data):

        # skip the two header lines
        for line in filter(None, jc.utils.splitlines(data)[2:]):
            interface, colon, values = line.partition(':')
            fields = values.split()
            if not colon or len(fields) != len(_FIELDS):
                raise ParseError(f'Unexpected line: {line}')

            entry = {'interface': interface.strip()}
            entry.update(zip(_FIELDS, fields))
            raw_output.append(entry)

    return raw_output if raw else _process(raw_output)
