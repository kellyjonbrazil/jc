r"""jc - JSON Convert `/proc/pagetypeinfo` file parser

Usage (cli):

    $ cat /proc/pagetypeinfo | jc --proc

or

    $ jc /proc/pagetypeinfo

or

    $ cat /proc/pagetypeinfo | jc --proc-pagetypeinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_pagetypeinfo_file)

or

    import jc
    result = jc.parse('proc_pagetypeinfo', proc_pagetypeinfo_file)

Schema:

    {
      "page_block_order":             integer,
      "pages_per_block":              integer,
      "free_pages": [
        {
          "node":                     integer,
          "zone":                     string,
          "type":                     string,
          "free": [
                                      integer  # [0]
          ]
      ],
      "num_blocks_type": [
        {
          "node":                     integer,
          "zone":                     string,
          "unmovable":                integer,
          "movable":                  integer,
          "reclaimable":              integer,
          "high_atomic":              integer,
          "isolate":                  integer
        }
      ]
    }

    [0] array index correlates to the Order number.
        E.g. free[0] is the value for Order 0

Examples:

    $ cat /proc/pagetypeinfo | jc --proc -p
    {
      "page_block_order": 9,
      "pages_per_block": 512,
      "free_pages": [
        {
          "node": 0,
          "zone": "DMA",
          "type": "Unmovable",
          "free": [
            0,
            0,
            0,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0
          ]
        },
        ...
      ],
      "num_blocks_type": [
        {
          "node": 0,
          "zone": "DMA",
          "unmovable": 1,
          "movable": 7,
          "reclaimable": 0,
          "high_atomic": 0,
          "isolate": 0
        },
        {
          "node": 0,
          "zone": "DMA32",
          "unmovable": 8,
          "movable": 1472,
          "reclaimable": 48,
          "high_atomic": 0,
          "isolate": 0
        },
        {
          "node": 0,
          "zone": "Normal",
          "unmovable": 120,
          "movable": 345,
          "reclaimable": 47,
          "high_atomic": 0,
          "isolate": 0
        }
      ]
    }
"""
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/pagetypeinfo` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}
    section = ''

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            if line.startswith('Page block order:'):
                raw_output['page_block_order'] = int(line.split(':', maxsplit=1)[1])
                continue

            if line.startswith('Pages per block:'):
                raw_output['pages_per_block'] = int(line.split(':', maxsplit=1)[1])
                continue

            if line.startswith('Free pages count per migrate type at order'):
                section = 'free_pages'
                raw_output['free_pages'] = []
                continue

            if line.startswith('Number of blocks type'):
                section = 'num_blocks_type'
                raw_output['num_blocks_type'] = []
                continue

            # Free pages count per migrate type at order       0      1      2      3      4      5      6      7      8      9     10
            # Node    0, zone      DMA, type    Unmovable      0      0      0      1      1      1      1      1      0      0      0
            if section == 'free_pages':
                split_line = line.replace(',', ' ').split()

                output_line = {
                    'node': int(split_line[1]),
                    'zone': split_line[3],
                    'type': split_line[5],
                    'free': [int(x) for x in split_line[6:]]
                }

                raw_output['free_pages'].append(output_line)
                continue

            # Number of blocks type     Unmovable      Movable  Reclaimable   HighAtomic      Isolate 
            # Node 0, zone      DMA            1            7            0            0            0 
            if section == 'num_blocks_type':
                split_line = line.replace(',', ' ').split()

                output_line = {
                    'node': int(split_line[1]),
                    'zone': split_line[3],
                    'unmovable': int(split_line[4]),
                    'movable': int(split_line[5]),
                    'reclaimable': int(split_line[6]),
                    'high_atomic': int(split_line[7]),
                    'isolate': int(split_line[8]),
                }

                raw_output['num_blocks_type'].append(output_line)
                continue

    return raw_output if raw else _process(raw_output)
