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
      "flags":                      integer,  # [0]
      "mnt_id":                     integer,
      "scm_fds":                    string,
      "ino":                        integer,
      "lock": [
                                    string
      ],
      "epoll": [
        {
          "tfd":                    integer,
          "events":                 string,
          "data":                   string,
          "pos":                    integer,
          "ino":                    string,
          "sdev":                   string
        }
      ],
      "inotify": [
        {
          "wd":                     integer,  # [1]
          "ino":                    string,
          "sdev":                   string,
          "mask":                   string,
          "ignored_mask":           string,
          "fhandle-bytes":          string,
          "fhandle-type":           string,
          "f_handle":               string
        }
      ],
      "fanotify": {
        "flags":                    string,
        "event-flags":              string,
        "marks": [
          {
            "mnt_id":               string,
            "mnt_ns":               string,
            "mflags":               string,
            "mask":                 string,
            "ignored_mask":         string,
            "ino":                  string,
            "sdev":                 string,
            "fhandle-bytes":        string,
            "fhandle-type":         string,
            "f_handle":             string
          }
        ]
      },
      "clockid":                    integer,
      "ticks":                      integer,
      "settime flags":              integer,  # [0]
      "it_value": [
                                    integer
      ],
      "it_interval": [
                                    integer
      ]
    }

    [0] converted from octal
    [1] converted from hexadecimal

Examples:

    $ cat /proc/1/fdinfo/5 | jc --proc -p
    {
      "pos": 0,
      "flags": 526336,
      "mnt_id": 19,
      "ino": 84,
      "inotify": [
        {
          "wd": 11,
          "ino": "9360d8",
          "sdev": "fc00000",
          "mask": "2",
          "ignored_mask": "0",
          "fhandle-bytes": "c",
          "fhandle-type": "81",
          "f_handle": "d8609300000000000ab79f4e"
        },
        {
          "wd": 10,
          "ino": "9360d7",
          "sdev": "fc00000",
          "mask": "2",
          "ignored_mask": "0",
          "fhandle-bytes": "c",
          "fhandle-type": "81",
          "f_handle": "d7609300000000005bcd4b8d"
        }
      ]
    }

    $ cat /proc/1/fdinfo/5 | jc --proc -p -r
    {
      "pos": "0",
      "flags": "02004000",
      "mnt_id": "19",
      "ino": "84",
      "inotify": [
        {
          "wd": "b",
          "ino": "9360d8",
          "sdev": "fc00000",
          "mask": "2",
          "ignored_mask": "0",
          "fhandle-bytes": "c",
          "fhandle-type": "81",
          "f_handle": "d8609300000000000ab79f4e"
        },
        {
          "wd": "a",
          "ino": "9360d7",
          "sdev": "fc00000",
          "mask": "2",
          "ignored_mask": "0",
          "fhandle-bytes": "c",
          "fhandle-type": "81",
          "f_handle": "d7609300000000005bcd4b8d"
        }
      ]
    }
"""
import re
from typing import Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '2.0'
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
    root_int_list = {'pos', 'mnt_id', 'ino', 'clockid', 'ticks', 'size', 'count'}
    root_octal_list = {'flags', 'settime flags'}
    epoll_int_list = {'tfd', 'pos'}
    inotify_hex_list = {'wd'}

    for key, val in proc_data.items():
        if key in root_int_list:
            proc_data[key] = int(val)

        if key in root_octal_list:
            proc_data[key] = int(val, 8)

    for item in proc_data.get('epoll', []):
        for key, val in item.items():
            if key in epoll_int_list:
                item[key] = int(val)

    for item in proc_data.get('inotify', []):
        for key, val in item.items():
            if key in inotify_hex_list:
                item[key] = int(val, 16)

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

        for line in filter(None, jc.utils.splitlines(data)):

            # epoll files
            if line.startswith('tfd:'):
                line_match = re.findall(r'(?<!\S)(?P<key>\S+):(?:\s+)?(?P<val>\S+s*)', line)
                if line_match:
                    raw_output.setdefault('epoll', []).append(
                        {k.strip(): v.strip() for k, v in line_match}
                    )
                continue

            # inotify files: one line per watch
            if line.startswith('inotify'):
                split_line = line[8:].split()
                watch = {}
                for item in split_line:
                    k, v = item.split(':', maxsplit=1)
                    watch[k] = v
                raw_output.setdefault('inotify', []).append(watch)
                continue

            # fanotify files: one group flags line, then one line per mark
            if line.startswith('fanotify'):
                split_line = line[9:].split()
                fanotify = raw_output.setdefault('fanotify', {})

                if split_line and split_line[0].startswith('flags:'):
                    fanotify_obj = fanotify
                else:
                    fanotify_obj = {}

                for item in split_line:
                    k, v = item.split(':', maxsplit=1)
                    fanotify_obj[k] = v

                marks = fanotify.setdefault('marks', [])
                if fanotify_obj is not fanotify:
                    marks.append(fanotify_obj)
                continue

            # file locks: one line per lock
            if line.startswith('lock:'):
                raw_output.setdefault('lock', []).append(line[5:].strip())
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
