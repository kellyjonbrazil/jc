r"""jc - JSON Convert `/proc/vmstat` file parser

Usage (cli):

    $ cat /proc/vmstat | jc --proc

or

    $ jc /proc/vmstat

or

    $ cat /proc/vmstat | jc --proc-vmstat

Usage (module):

    import jc
    result = jc.parse('proc', proc_vmstat_file)

or

    import jc
    result = jc.parse('proc_vmstat', proc_vmstat_file)

Schema:

All values are integers.

    {
      <keyName>             integer
    }

Examples:

    $ cat /proc/vmstat | jc --proc -p
    {
      "nr_free_pages": 615337,
      "nr_zone_inactive_anon": 39,
      "nr_zone_active_anon": 34838,
      "nr_zone_inactive_file": 104036,
      "nr_zone_active_file": 130601,
      "nr_zone_unevictable": 4897,
      "nr_zone_write_pending": 45,
      "nr_mlock": 4897,
      "nr_page_table_pages": 548,
      "nr_kernel_stack": 5984,
      "nr_bounce": 0,
      "nr_zspages": 0,
      "nr_free_cma": 0,
      "numa_hit": 1910597,
      "numa_miss": 0,
      "numa_foreign": 0,
      ...
    }
"""
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/vmstat` file parser'
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

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            key, val = line.split(maxsplit=1)
            raw_output[key] = int(val)

    return raw_output if raw else _process(raw_output)
