"""jc - JSON Convert `/proc/stat` file parser

Usage (cli):

    $ cat /proc/stat | jc --proc

or

    $ jc /proc/stat

or

    $ cat /proc/stat | jc --proc-stat

Usage (module):

    import jc
    result = jc.parse('proc', proc_stat_file)

or

    import jc
    result = jc.parse('proc_stat', proc_stat_file)

Schema:

    {
      "cpu": {
        "user":                         integer,
        "nice":                         integer,
        "system":                       integer,
        "idle":                         integer,
        "iowait":                       integer,
        "irq":                          integer,
        "softirq":                      integer,
        "steal":                        integer,
        "guest":                        integer,
        "guest_nice":                   integer
      },
      "cpu<number>": {
        "user":                         integer,
        "nice":                         integer,
        "system":                       integer,
        "idle":                         integer,
        "iowait":                       integer,
        "irq":                          integer,
        "softirq":                      integer,
        "steal":                        integer,
        "guest":                        integer,
        "guest_nice":                   integer
      },
      "interrupts": [
                                        integer
      ],
      "context_switches":               integer,
      "boot_time":                      integer,
      "processes":                      integer,
      "processes_running":              integer,
      "processes_blocked":              integer,
      "softirq": [
                                        integer
      ]
    }

Examples:

    $ cat /proc/stat | jc --proc -p
    {
      "cpu": {
        "user": 6002,
        "nice": 152,
        "system": 8398,
        "idle": 3444436,
        "iowait": 448,
        "irq": 0,
        "softirq": 1174,
        "steal": 0,
        "guest": 0,
        "guest_nice": 0
      },
      "cpu0": {
        "user": 2784,
        "nice": 137,
        "system": 4367,
        "idle": 1732802,
        "iowait": 225,
        "irq": 0,
        "softirq": 221,
        "steal": 0,
        "guest": 0,
        "guest_nice": 0
      },
      "cpu1": {
        "user": 3218,
        "nice": 15,
        "system": 4031,
        "idle": 1711634,
        "iowait": 223,
        "irq": 0,
        "softirq": 953,
        "steal": 0,
        "guest": 0,
        "guest_nice": 0
      },
      "interrupts": [
        2496709,
        18,
        73,
        0,
        0,
        ...
      ],
      "context_switches": 4622716,
      "boot_time": 1662154781,
      "processes": 9831,
      "processes_running": 1,
      "processes_blocked": 0,
      "softirq": [
        3478985,
        35230,
        1252057,
        3467,
        128583,
        51014,
        0,
        171199,
        1241297,
        0,
        596138
      ]
    }
"""
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/stat` file parser'
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

            if line.startswith('cpu'):
                split_line = line.split()
                cpu_num = split_line[0]
                raw_output[cpu_num] = {
                    'user': int(split_line[1]),
                    'nice': int(split_line[2]),
                    'system': int(split_line[3]),
                    'idle': int(split_line[4])
                }

                if len(split_line) > 5:
                    raw_output[cpu_num]['iowait'] = int(split_line[5])

                if len(split_line) > 6:
                    raw_output[cpu_num]['irq'] = int(split_line[6])
                    raw_output[cpu_num]['softirq'] = int(split_line[7])

                if len(split_line) > 8:
                    raw_output[cpu_num]['steal'] = int(split_line[8])

                if len(split_line) > 9:
                    raw_output[cpu_num]['guest'] = int(split_line[9])

                if len(split_line) > 10:
                    raw_output[cpu_num]['guest_nice'] = int(split_line[10])

                continue

            if line.startswith('intr '):
                split_line = line.split()
                raw_output['interrupts'] = [int(x) for x in split_line[1:]]
                continue

            if line.startswith('ctxt '):
                raw_output['context_switches'] = int(line.split(maxsplit=1)[1])
                continue

            if line.startswith('btime '):
                raw_output['boot_time'] = int(line.split(maxsplit=1)[1])
                continue

            if line.startswith('processes '):
                raw_output['processes'] = int(line.split(maxsplit=1)[1])
                continue

            if line.startswith('procs_running '):
                raw_output['processes_running'] = int(line.split(maxsplit=1)[1])
                continue

            if line.startswith('procs_blocked '):
                raw_output['processes_blocked'] = int(line.split(maxsplit=1)[1])
                continue

            if line.startswith('softirq '):
                split_line = line.split()
                raw_output['softirq'] = [int(x) for x in split_line[1:]]
                continue

    return raw_output if raw else _process(raw_output)
