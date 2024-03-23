r"""jc - JSON Convert `/proc/<pid>/fdinfo/<fd>` file parser

Usage (cli):

    $ cat /proc/1/fdinfo/5 | jc --proc

or

    $ jc /proc/1/fdinfo/5

or

    $ cat /proc/1/fdinfo/5 | jc --proc-pid-fdinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_pid_fdinfo_file)

or

    import jc
    result = jc.parse('proc_pid_fdinfo', proc_pid_fdinfo_file)

Schema:

Any unspecified fields are strings.

    {
      "pos":                        integer,
      "flags":                      integer,
      "mnt_id":                     integer,
      "scm_fds":                    string,
      "ino":                        integer,
      "lock":                       string,
      "epoll": {
        "tfd":                      integer,
        "events":                   string,
        "data":                     string,
        "pos":                      integer,
        "ino":                      string,
        "sdev":                     string
      },
      "inotify": {
        "wd":                       integer,
        "ino":                      string,
        "sdev":                     string,
        "mask":                     string,
        "ignored_mask":             string,
        "fhandle-bytes":            string,
        "fhandle-type":             string,
        "f_handle":                 string
      },
      "fanotify": {
        "flags":                    string,
        "event-flags":              string,
        "mnt_id":                   string,
        "mflags":                   string,
        "mask":                     string,
        "ignored_mask":             string,
        "ino":                      string,
        "sdev":                     string,
        "fhandle-bytes":            string,
        "fhandle-type":             string,
        "f_handle":                 string
      },
      "clockid":                    integer,
      "ticks":                      integer,
      "settime flags":              integer,
      "it_value": [
                                    integer
      ],
      "it_interval": [
                                    integer
      ]
    }

Examples:

    $ cat /proc/1/fdinfo/5 | jc --proc -p
    {
      "pos": 0,
      "flags": 2,
      "mnt_id": 9,
      "ino": 63107,
      "clockid": 0,
      "ticks": 0,
      "settime flags": 1,
      "it_value": [
        0,
        49406829
      ],
      "it_interval": [
        1,
        0
      ]
    }
"""
import re
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/<pid>/fdinfo/<fd>` file parser'
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

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    root_int_list = {'pos', 'flags', 'mnt_id', 'ino', 'clockid', 'ticks',
                     'settime flags', 'size', 'count'}
    epoll_int_list = {'tfd', 'pos'}
    inotify_int_list = {'wd'}

    for key, val in proc_data.items():
        if key in root_int_list:
            proc_data[key] = int(val)

    if 'epoll' in proc_data:
        for key, val in proc_data['epoll'].items():
            if key in epoll_int_list:
                proc_data['epoll'][key] = int(val)

    if 'inotify' in proc_data:
        for key, val in proc_data['inotify'].items():
            if key in inotify_int_list:
                proc_data['inotify'][key] = int(val)

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
    split_me = {'it_value:', 'it_interval:'}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            # epoll files
            if line.startswith('tfd:'):
                line_match = re.findall(r'(?P<key>\S+):(?:\s+)?(?P<val>\S+s*)', line)
                if line_match:
                    raw_output.update({'epoll': {k.strip(): v.strip() for k, v in line_match}})
                continue

            # inotify files
            if line.startswith('inotify'):
                split_line = line[8:].split()
                raw_output['inotify'] = {}
                for item in split_line:
                    k, v = item.split(':', maxsplit=1)
                    raw_output['inotify'][k] = v
                continue

            # fanotify files
            if line.startswith('fanotify'):
                split_line = line[9:].split()

                if not 'fanotify' in raw_output:
                    raw_output['fanotify'] = {}

                for item in split_line:
                    k, v = item.split(':', maxsplit=1)
                    raw_output['fanotify'][k] = v
                continue

            # timerfd files
            if line.split()[0] in split_me:
                split_line = line.replace(':', '').replace('(', '').replace(')', '').replace(',', '').split()
                raw_output[split_line[0]] = [int(x) for x in split_line[1:]]
                continue

            key, val = line.split(':', maxsplit=1)
            raw_output[key.strip()] = val.strip()
            continue

    return raw_output if raw else _process(raw_output)
