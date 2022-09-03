"""jc - JSON Convert Proc file output parser

<<Short procfile description and caveats>>

Usage (cli):

    $ cat /proc/<file> | jc --procfile

Usage (module):

    import jc
    result = jc.parse('procfile', proc_file)

Schema:

    [
      {
        "procfile":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ procfile | jc --procfile -p
    []

    $ procfile | jc --procfile -p -r
    []
"""
import re
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = 'Proc file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool
    # conversions and timestamps

    return proc_data


def _parse_uptime():
    print('uptime')


def _parse_loadavg():
    print('loadavg')


def _parse_cpuinfo():
    print('cpuinfo')


def _parse_meminfo():
    print('meminfo')


def _parse_version():
    print('version')


def _parse_crypto():
    print('crypto')


def _parse_diskstats():
    print('diskstats')


def _parse_filesystems():
    print('filesystems')


def _parse_pid_status():
    print('pid status')


def _parse_pid_statm():
    print('pid statm')


def _parse_pid_stat():
    print('pid stat')


def _parse_pid_smaps():
    print('pid smaps')


def _parse_pid_maps():
    print('pid maps')


def _parse_pid_numa_maps():
    print('pid numa_maps')


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

        # signatures
        uptime_p = re.compile(r'^\d+.\d\d \d+.\d\d$')
        loadavg_p = re.compile(r'^\d+.\d\d \d+.\d\d \d+.\d\d \d+/\d+ \d+$')
        cpuinfo_p = re.compile(r'^processor\s+:.*\nvendor_id\s+:.*\ncpu family\s+:.*\n')
        meminfo_p = re.compile(r'^MemTotal:.*\nMemFree:.*\nMemAvailable:.*\n')
        version_p = re.compile(r'^.+\sversion\s[^\n]+$')
        crypto_p = re.compile(r'^name\s+:.*\ndriver\s+:.*\nmodule\s+:.*\n')
        diskstats_p = re.compile(r'^\s*\d+\s+\d\s\w+\s(?:\d+\s){16}\d\n')
        filesystems_p = re.compile(r'^(?:(?:nodev\t|\t)\w+\n){3}')
        pid_status_p = re.compile(r'^Name:\t.+\nUmask:\t\d+\nState:\t.+\nTgid:\t\d+\n')
        pid_statm_p = re.compile(r'^\d+ \d+ \d+\s\d+\s\d+\s\d+\s\d+$')
        pid_stat_p = re.compile(r'^\d+ \(.{1,16}\) \w \d+ \d+ \d+ \d+ -?\d+ (?:\d+ ){43}\d+$')
        pid_smaps_p = re.compile(r'^[0-9a-f]{12}-[0-9a-f]{12} [rwxsp\-]{4} [0-9a-f]{8} [0-9a-f]{2}:[0-9a-f]{2} \d+ [^\n]+\nSize:\s+\d+ \S\S\n')
        pid_maps_p = re.compile(r'^[0-9a-f]{12}-[0-9a-f]{12} [rwxsp\-]{4} [0-9a-f]{8} [0-9a-f]{2}:[0-9a-f]{2} \d+ ')
        pid_numa_maps_p = re.compile(r'^[a-f0-9]{12} default [^\n]+\n')

        procmap = {
            uptime_p: _parse_uptime,
            loadavg_p: _parse_loadavg,
            cpuinfo_p: _parse_cpuinfo,
            meminfo_p: _parse_meminfo,
            version_p: _parse_version,
            crypto_p: _parse_crypto,
            diskstats_p: _parse_diskstats,
            filesystems_p: _parse_filesystems,
            pid_status_p: _parse_pid_status,
            pid_statm_p: _parse_pid_statm,
            pid_stat_p: _parse_pid_stat,
            pid_smaps_p: _parse_pid_smaps,  # before pid_maps
            pid_maps_p: _parse_pid_maps,    # after pid_smaps
            pid_numa_maps_p: _parse_pid_numa_maps
        }

        for reg_pattern, parse_func in procmap.items():
            if reg_pattern.search(data):
                parse_func()
                break

        # for line in filter(None, data.splitlines()):

        #     # parse the content here
        #     # check out helper functions in jc.utils
        #     # and jc.parsers.universal

        #     pass

    return raw_output if raw else _process(raw_output)
