r"""jc - JSON Convert `/proc/slabinfo` file parser

Usage (cli):

    $ cat /proc/slabinfo | jc --proc

or

    $ jc /proc/slabinfo

or

    $ cat /proc/slabinfo | jc --proc-slabinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_slabinfo_file)

or

    import jc
    result = jc.parse('proc_slabinfo', proc_slabinfo_file)

Schema:

    [
      {
        "name":                             string,
        "active_objs":                      integer,
        "num_objs":                         integer,
        "obj_size":                         integer,
        "obj_per_slab":                     integer,
        "pages_per_slab":                   integer,
        "tunables": {
          "limit":                          integer,
          "batch_count":                    integer,
          "shared_factor":                  integer
        },
        "slabdata": {
          "active_slabs":                   integer,
          "num_slabs":                      integer,
          "shared_avail":                   integer
      }
    ]

Examples:

    $ cat /proc/slabinfo | jc --proc -p
    [
      {
        "name": "ext4_groupinfo_4k",
        "active_objs": 224,
        "num_objs": 224,
        "obj_size": 144,
        "obj_per_slab": 56,
        "pages_per_slab": 2,
        "tunables": {
          "limit": 0,
          "batch_count": 0,
          "shared_factor": 0
        },
        "slabdata": {
          "active_slabs": 4,
          "num_slabs": 4,
          "shared_avail": 0
        }
      },
      ...
    ]
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/slabinfo` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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

    raw_output: List = []

    if jc.utils.has_data(data):

        cleandata = data.splitlines()[2:]

        for line in filter(None, cleandata):

            line = line.replace(':', ' ')
            split_line = line.split()

            raw_output.append(
                {
                    'name': split_line[0],
                    'active_objs': int(split_line[1]),
                    'num_objs': int(split_line[2]),
                    'obj_size': int(split_line[3]),
                    'obj_per_slab': int(split_line[4]),
                    'pages_per_slab': int(split_line[5]),
                    'tunables': {
                        'limit': int(split_line[7]),
                        'batch_count': int(split_line[8]),
                        'shared_factor': int(split_line[9])
                    },
                    'slabdata': {
                        'active_slabs': int(split_line[11]),
                        'num_slabs': int(split_line[12]),
                        'shared_avail': int(split_line[13])
                    }
                }
            )

    return raw_output if raw else _process(raw_output)
