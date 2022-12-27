"""jc - JSON Convert `/proc/zoneinfo` file parser

Usage (cli):

    $ cat /proc/zoneinfo | jc --proc

or

    $ jc /proc/zoneinfo

or

    $ cat /proc/zoneinfo | jc --proc-zoneinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_zoneinfo_file)

or

    import jc
    result = jc.parse('proc_zoneinfo', proc_zoneinfo_file)

Schema:

All values are integers.

    [
      {
        "node":                               integer,
        "<zone>": {
          "pages": {
            "free":                           integer,
            "min":                            integer,
            "low":                            integer,
            "high":                           integer,
            "spanned":                        integer,
            "present":                        integer,
            "managed":                        integer,
            "protection": [
                                              integer
            ],
            "<key>":                          integer
          },
          "pagesets": [
            {
              "cpu":                          integer,
              "count":                        integer,
              "high":                         integer,
              "batch":                        integer,
              "vm stats threshold":           integer,
              "<key>":                        integer
            }
          ]
        },
        "<key>":                              integer,  # [0]
      }
    ]

    [0] per-node stats

Examples:

    $ cat /proc/zoneinfo | jc --proc -p
    [
      {
        "node": 0,
        "DMA": {
          "pages": {
            "free": 3832,
            "min": 68,
            "low": 85,
            "high": 102,
            "spanned": 4095,
            "present": 3997,
            "managed": 3976,
            "protection": [
              0,
              2871,
              3795,
              3795,
              3795
            ],
            "nr_free_pages": 3832,
            "nr_zone_inactive_anon": 0,
            "nr_zone_active_anon": 0,
            "nr_zone_inactive_file": 0,
            "nr_zone_active_file": 0,
            "nr_zone_unevictable": 0,
            "nr_zone_write_pending": 0,
            "nr_mlock": 0,
            "nr_page_table_pages": 0,
            "nr_kernel_stack": 0,
            "nr_bounce": 0,
            "nr_zspages": 0,
            "nr_free_cma": 0,
            "numa_hit": 3,
            "numa_miss": 0,
            "numa_foreign": 0,
            "numa_interleave": 1,
            "numa_local": 3,
            "numa_other": 0
          },
          "pagesets": [
            {
              "cpu": 0,
              "count": 0,
              "high": 0,
              "batch": 1,
              "vm stats threshold": 4
            },
            {
              "cpu": 1,
              "count": 0,
              "high": 0,
              "batch": 1,
              "vm stats threshold": 4,
              "node_unreclaimable": 0,
              "start_pfn": 1
            }
          ]
        },
        "nr_inactive_anon": 39,
        "nr_active_anon": 34839,
        "nr_inactive_file": 104172,
        "nr_active_file": 130748,
        "nr_unevictable": 4897,
        "nr_slab_reclaimable": 49017,
        "nr_slab_unreclaimable": 26177,
        "nr_isolated_anon": 0,
        "nr_isolated_file": 0,
        "workingset_nodes": 0,
        "workingset_refault": 0,
        "workingset_activate": 0,
        "workingset_restore": 0,
        "workingset_nodereclaim": 0,
        "nr_anon_pages": 40299,
        "nr_mapped": 25140,
        "nr_file_pages": 234396,
        "nr_dirty": 0,
        "nr_writeback": 0,
        "nr_writeback_temp": 0,
        "nr_shmem": 395,
        "nr_shmem_hugepages": 0,
        "nr_shmem_pmdmapped": 0,
        "nr_file_hugepages": 0,
        "nr_file_pmdmapped": 0,
        "nr_anon_transparent_hugepages": 0,
        "nr_vmscan_write": 0,
        "nr_vmscan_immediate_reclaim": 0,
        "nr_dirtied": 168223,
        "nr_written": 144616,
        "nr_kernel_misc_reclaimable": 0,
        "nr_foll_pin_acquired": 0,
        "nr_foll_pin_released": 0,
        "DMA32": {
          "pages": {
            "free": 606010,
            "min": 12729,
            "low": 15911,
            "high": 19093,
            "spanned": 1044480,
            "present": 782288,
            "managed": 758708,
            "protection": [
              0,
              0,
              924,
              924,
              924
            ],
            "nr_free_pages": 606010,
            "nr_zone_inactive_anon": 4,
            "nr_zone_active_anon": 17380,
            "nr_zone_inactive_file": 41785,
            "nr_zone_active_file": 64545,
            "nr_zone_unevictable": 5,
            "nr_zone_write_pending": 0,
            "nr_mlock": 5,
            "nr_page_table_pages": 101,
            "nr_kernel_stack": 224,
            "nr_bounce": 0,
            "nr_zspages": 0,
            "nr_free_cma": 0,
            "numa_hit": 576595,
            "numa_miss": 0,
            "numa_foreign": 0,
            "numa_interleave": 2,
            "numa_local": 576595,
            "numa_other": 0
          },
          "pagesets": [
            {
              "cpu": 0,
              "count": 253,
              "high": 378,
              "batch": 63,
              "vm stats threshold": 24
            },
            {
              "cpu": 1,
              "count": 243,
              "high": 378,
              "batch": 63,
              "vm stats threshold": 24,
              "node_unreclaimable": 0,
              "start_pfn": 4096
            }
          ]
        },
        "Normal": {
          "pages": {
            "free": 5113,
            "min": 4097,
            "low": 5121,
            "high": 6145,
            "spanned": 262144,
            "present": 262144,
            "managed": 236634,
            "protection": [
              0,
              0,
              0,
              0,
              0
            ],
            "nr_free_pages": 5113,
            "nr_zone_inactive_anon": 35,
            "nr_zone_active_anon": 17459,
            "nr_zone_inactive_file": 62387,
            "nr_zone_active_file": 66203,
            "nr_zone_unevictable": 4892,
            "nr_zone_write_pending": 0,
            "nr_mlock": 4892,
            "nr_page_table_pages": 447,
            "nr_kernel_stack": 5760,
            "nr_bounce": 0,
            "nr_zspages": 0,
            "nr_free_cma": 0,
            "numa_hit": 1338441,
            "numa_miss": 0,
            "numa_foreign": 0,
            "numa_interleave": 66037,
            "numa_local": 1338441,
            "numa_other": 0
          },
          "pagesets": [
            {
              "cpu": 0,
              "count": 340,
              "high": 378,
              "batch": 63,
              "vm stats threshold": 16
            },
            {
              "cpu": 1,
              "count": 174,
              "high": 378,
              "batch": 63,
              "vm stats threshold": 16,
              "node_unreclaimable": 0,
              "start_pfn": 1048576
            }
          ]
        },
        "Movable": {
          "pages": {
            "free": 0,
            "min": 0,
            "low": 0,
            "high": 0,
            "spanned": 0,
            "present": 0,
            "managed": 0,
            "protection": [
              0,
              0,
              0,
              0,
              0
            ]
          }
        },
        "Device": {
          "pages": {
            "free": 0,
            "min": 0,
            "low": 0,
            "high": 0,
            "spanned": 0,
            "present": 0,
            "managed": 0,
            "protection": [
              0,
              0,
              0,
              0,
              0
            ]
          }
        }
      }
    ]
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/zoneinfo` file parser'
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
    ouptput_line: Dict = {}
    node = None
    section = 'stats'    # stats, pages, pagesets
    pageset = None

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            if line == '  per-node stats':
                continue

            if line.startswith('Node ') and line.endswith('DMA'):
                if ouptput_line:
                    raw_output.append(ouptput_line)
                    ouptput_line = {}

                section = 'stats'
                _, node, _, zone = line.replace(',', '').split()
                ouptput_line['node'] = int(node)
                ouptput_line[zone] = {}
                continue

            if line.startswith('Node '):
                section = 'stats'

                if pageset:
                    ouptput_line[zone]['pagesets'].append(pageset)
                    pageset = {}

                _, node, _, zone = line.replace(',', '').split()
                ouptput_line['node'] = int(node)
                ouptput_line[zone] = {}
                continue

            if line.startswith('  pages free '):
                section = 'pages'
                ouptput_line[zone]['pages'] = {}
                ouptput_line[zone]['pages']['free'] = int(line.split()[-1])
                continue

            if line.startswith('  pagesets'):
                section = 'pagesets'
                ouptput_line[zone]['pagesets'] = []
                pageset = {}  # type: ignore
                continue

            if section == 'stats':
                key, val = line.split(maxsplit=1)
                ouptput_line[key] = int(val)
                continue

            if section == 'pages' and line.startswith('        protection: '):
                protection = line.replace('(', '').replace(')', '').replace(',', '').split()[1:]
                ouptput_line[zone]['pages']['protection'] = [int(x) for x in protection]
                continue

            if section == 'pages':
                key, val = line.split(maxsplit=1)
                ouptput_line[zone]['pages'][key] = int(val)
                continue

            if section == 'pagesets' and line.startswith('    cpu: '):
                if pageset:
                    ouptput_line[zone]['pagesets'].append(pageset)

                split_line = line.replace(':', '').split(maxsplit=1)
                pageset = {"cpu": int(split_line[1])}
                continue

            if section == 'pagesets':
                key, val = line.split(':', maxsplit=1)
                pageset[key.strip()] = int(val)
                continue

        if ouptput_line:
            if pageset:
                ouptput_line[zone]['pagesets'].append(pageset)

            raw_output.append(ouptput_line)

    return raw_output if raw else _process(raw_output)
