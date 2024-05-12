r"""jc - JSON Convert `top -b` command output parser

Requires batch mode (`-b`). The `-n` option must also be used to limit
the number of times `top` is run.

Warning messages will be printed to `STDERR` if truncated fields are
detected. These warnings can be suppressed with the `-q` or `quiet=True`
option.

Usage (cli):

    $ top -b -n 3 | jc --top

or

    $ jc top -b -n 3

Usage (module):

    import jc
    result = jc.parse('top', top_command_output)

Schema:

All `-` values are converted to `null`

    [
      {
        "time":                                         string,
        "uptime":                                       integer,
        "users":                                        integer,
        "load_1m":                                      float,
        "load_5m":                                      float,
        "load_15m":                                     float,
        "tasks_total":                                  integer,
        "tasks_running":                                integer,
        "tasks_sleeping":                               integer,
        "tasks_stopped":                                integer,
        "tasks_zombie":                                 integer,
        "cpu_user":                                     float,
        "cpu_sys":                                      float,
        "cpu_nice":                                     float,
        "cpu_idle":                                     float,
        "cpu_wait":                                     float,
        "cpu_hardware":                                 float,
        "cpu_software":                                 float,
        "cpu_steal":                                    float,
        "mem_total":                                    float,    # [0]
        "mem_free":                                     float,    # [0]
        "mem_used":                                     float,    # [0]
        "mem_buff_cache":                               float,    # [0]
        "swap_total":                                   float,    # [0]
        "swap_free":                                    float,    # [0]
        "swap_used":                                    float,    # [0]
        "mem_available":                                float,    # [0]
        "processes": [
          {
            "pid":                                      integer,
            "user":                                     string,
            "priority":                                 integer,
            "nice":                                     integer,
            "virtual_mem":                              float,    # [1]
            "resident_mem":                             float,    # [1]
            "shared_mem":                               float,    # [1]
            "status":                                   string,
            "percent_cpu":                              float,
            "percent_mem":                              float,
            "time_hundredths":                          string,
            "command":                                  string,
            "parent_pid":                               integer,
            "uid":                                      integer,
            "real_uid":                                 integer,
            "real_user":                                string,
            "saved_uid":                                integer,
            "saved_user":                               string,
            "gid":                                      integer,
            "group":                                    string,
            "pgrp":                                     integer,
            "tty":                                      string,
            "tty_process_gid":                          integer,
            "session_id":                               integer,
            "thread_count":                             integer,
            "last_used_processor":                      integer,
            "time":                                     string,
            "swap":                                     float,    # [1]
            "code":                                     float,    # [1]
            "data":                                     float,    # [1]
            "major_page_fault_count":                   integer,
            "minor_page_fault_count":                   integer,
            "dirty_pages_count":                        integer,
            "sleeping_in_function":                     string,
            "flags":                                    string,
            "cgroups":                                  string,
            "supplementary_gids": [
                                                        integer
            ],
            "supplementary_groups": [
                                                        string
            ],
            "thread_gid":                               integer,
            "environment_variables": [
                                                        string
            ]
            "major_page_fault_count_delta":             integer,
            "minor_page_fault_count_delta":             integer,
            "used":                                     float,    # [1]
            "ipc_namespace_inode":                      integer,
            "mount_namespace_inode":                    integer,
            "net_namespace_inode":                      integer,
            "pid_namespace_inode":                      integer,
            "user_namespace_inode":                     integer,
            "nts_namespace_inode":                      integer,
            "control_group_name":                       string,
            "lxc_container_name":                       string,
            "numa_node":                                integer,
            "out_of_mem_adjustment":                    integer,
            "out_of_mem_score":                         integer,
            "resident_anon_mem":                        integer,
            "resident_file_backed_mem":                 integer,
            "resident_locked_mem":                      integer,
            "resident_shared_mem":                      integer
          }
        ]
      }
    ]

    [0] Values are in the units output by `top`
    [1] Unit suffix stripped during float conversion

Examples:

    $ top -b -n 3 | jc --top -p
    [
      {
        "time": "11:20:43",
        "uptime": 118,
        "users": 2,
        "load_1m": 0.0,
        "load_5m": 0.01,
        "load_15m": 0.05,
        "tasks_total": 108,
        "tasks_running": 2,
        "tasks_sleeping": 106,
        "tasks_stopped": 0,
        "tasks_zombie": 0,
        "cpu_user": 5.6,
        "cpu_sys": 11.1,
        "cpu_nice": 0.0,
        "cpu_idle": 83.3,
        "cpu_wait": 0.0,
        "cpu_hardware": 0.0,
        "cpu_software": 0.0,
        "cpu_steal": 0.0,
        "mem_total": 3.7,
        "mem_free": 3.3,
        "mem_used": 0.2,
        "mem_buff_cache": 0.2,
        "swap_total": 2.0,
        "swap_free": 2.0,
        "swap_used": 0.0,
        "mem_available": 3.3,
        "processes": [
          {
            "pid": 2225,
            "user": "kbrazil",
            "priority": 20,
            "nice": 0,
            "virtual_mem": 158.1,
            "resident_mem": 2.2,
            "shared_mem": 1.6,
            "status": "running",
            "percent_cpu": 12.5,
            "percent_mem": 0.1,
            "time_hundredths": "0:00.02",
            "command": "top",
            "parent_pid": 1884,
            "uid": 1000,
            "real_uid": 1000,
            "real_user": "kbrazil",
            "saved_uid": 1000,
            "saved_user": "kbrazil",
            "gid": 1000,
            "group": "kbrazil",
            "pgrp": 2225,
            "tty": "pts/0",
            "tty_process_gid": 2225,
            "session_id": 1884,
            "thread_count": 1,
            "last_used_processor": 0,
            "time": "0:00",
            "swap": 0.0,
            "code": 0.1,
            "data": 1.0,
            "major_page_fault_count": 0,
            "minor_page_fault_count": 736,
            "dirty_pages_count": 0,
            "sleeping_in_function": null,
            "flags": "..4.2...",
            "cgroups": "1:name=systemd:/user.slice/user-1000.+",
            "supplementary_gids": [
              10,
              1000
            ],
            "supplementary_groups": [
              "wheel",
              "kbrazil"
            ],
            "thread_gid": 2225,
            "environment_variables": [
              "XDG_SESSION_ID=2",
              "HOSTNAME=localhost"
            ],
            "major_page_fault_count_delta": 0,
            "minor_page_fault_count_delta": 4,
            "used": 2.2,
            "ipc_namespace_inode": 4026531839,
            "mount_namespace_inode": 4026531840,
            "net_namespace_inode": 4026531956,
            "pid_namespace_inode": 4026531836,
            "user_namespace_inode": 4026531837,
            "nts_namespace_inode": 4026531838
          },
          ...
        ]
      }
    ]

    $ top -b -n 3 | jc --top -p -r
    [
      {
        "time": "11:20:43",
        "uptime": "1:18",
        "users": "2",
        "load_1m": "0.00",
        "load_5m": "0.01",
        "load_15m": "0.05",
        "tasks_total": "108",
        "tasks_running": "2",
        "tasks_sleeping": "106",
        "tasks_stopped": "0",
        "tasks_zombie": "0",
        "cpu_user": "5.6",
        "cpu_sys": "11.1",
        "cpu_nice": "0.0",
        "cpu_idle": "83.3",
        "cpu_wait": "0.0",
        "cpu_hardware": "0.0",
        "cpu_software": "0.0",
        "cpu_steal": "0.0",
        "swap_total": "2.0",
        "swap_free": "2.0",
        "swap_used": "0.0",
        "mem_available": "3.3",
        "processes": [
          {
            "PID": "2225",
            "USER": "kbrazil",
            "PR": "20",
            "NI": "0",
            "VIRT": "158.1m",
            "RES": "2.2m",
            "SHR": "1.6m",
            "S": "R",
            "%CPU": "12.5",
            "%MEM": "0.1",
            "TIME+": "0:00.02",
            "COMMAND": "top",
            "PPID": "1884",
            "UID": "1000",
            "RUID": "1000",
            "RUSER": "kbrazil",
            "SUID": "1000",
            "SUSER": "kbrazil",
            "GID": "1000",
            "GROUP": "kbrazil",
            "PGRP": "2225",
            "TTY": "pts/0",
            "TPGID": "2225",
            "SID": "1884",
            "nTH": "1",
            "P": "0",
            "TIME": "0:00",
            "SWAP": "0.0m",
            "CODE": "0.1m",
            "DATA": "1.0m",
            "nMaj": "0",
            "nMin": "736",
            "nDRT": "0",
            "WCHAN": "-",
            "Flags": "..4.2...",
            "CGROUPS": "1:name=systemd:/user.slice/user-1000.+",
            "SUPGIDS": "10,1000",
            "SUPGRPS": "wheel,kbrazil",
            "TGID": "2225",
            "ENVIRON": "XDG_SESSION_ID=2 HOSTNAME=localhost S+",
            "vMj": "0",
            "vMn": "4",
            "USED": "2.2m",
            "nsIPC": "4026531839",
            "nsMNT": "4026531840",
            "nsNET": "4026531956",
            "nsPID": "4026531836",
            "nsUSER": "4026531837",
            "nsUTS": "4026531838"
          },
          ...
        ]
      }
    ]
"""
from typing import List, Dict, Set
import jc.utils
from jc.parsers.uptime import parse as parse_uptime
from jc.parsers.universal import sparse_table_parse as parse_table


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`top -b` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['top -b']
    tags = ['command']


__version__ = info.version


def _safe_split(string: str, path: str, delim: str = ' ', quiet=False) -> List[str]:
    split_string = string.split(delim)
    split_string = [x for x in split_string if not x.endswith('+')]

    if string.endswith('+') and not quiet:
        jc.utils.warning_message([f'{path} list was truncated by top'])

    return split_string


def _process(proc_data: List[Dict], quiet=False) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    key_map: Dict = {
        '%CPU': 'percent_cpu',
        '%MEM': 'percent_mem',
        'CGNAME': 'control_group_name',
        'CGROUPS': 'cgroups',
        'CODE': 'code',
        'COMMAND': 'command',
        'DATA': 'data',
        'ENVIRON': 'environment_variables',
        'Flags': 'flags',
        'GID': 'gid',
        'GROUP': 'group',
        'LXC': 'lxc_container_name',
        'NI': 'nice',
        'NU': 'numa_node',
        'OOMa': 'out_of_mem_adjustment',
        'OOMs': 'out_of_mem_score',
        'P': 'last_used_processor',
        'PGRP': 'pgrp',
        'PID': 'pid',
        'PPID': 'parent_pid',
        'PR': 'priority',
        'RES': 'resident_mem',
        'RSan': 'resident_anon_mem',
        'RSfd': 'resident_file_backed_mem',
        'RSlk': 'resident_locked_mem',
        'RSsh': 'resident_shared_mem',
        'RUID': 'real_uid',
        'RUSER': 'real_user',
        'S': 'status',
        'SHR': 'shared_mem',
        'SID': 'session_id',
        'SUID': 'saved_uid',
        'SUPGIDS': 'supplementary_gids',
        'SUPGRPS': 'supplementary_groups',
        'SUSER': 'saved_user',
        'SWAP': 'swap',
        'TGID': 'thread_gid',
        'TIME': 'time',
        'TIME+': 'time_hundredths',
        'TPGID': 'tty_process_gid',
        'TTY': 'tty',
        'UID': 'uid',
        'USED': 'used',
        'USER': 'user',
        'VIRT': 'virtual_mem',
        'WCHAN': 'sleeping_in_function',
        'nDRT': 'dirty_pages_count',
        'nMaj': 'major_page_fault_count',
        'nMin': 'minor_page_fault_count',
        'nTH': 'thread_count',
        'nsIPC': 'ipc_namespace_inode',
        'nsMNT': 'mount_namespace_inode',
        'nsNET': 'net_namespace_inode',
        'nsPID': 'pid_namespace_inode',
        'nsUSER': 'user_namespace_inode',
        'nsUTS': 'nts_namespace_inode',
        'vMj': 'major_page_fault_count_delta',
        'vMn': 'minor_page_fault_count_delta'
    }

    status_map: Dict = {
        'D': 'uninterruptible sleep',
        'I': 'idle',
        'R': 'running',
        'S': 'sleeping',
        'T': 'stopped by job control signal',
        't': 'stopped by debugger during trace',
        'Z': 'zombie'
    }

    int_list: Set = {
        'uptime', 'users', 'tasks_total', 'tasks_running', 'tasks_sleeping', 'tasks_stopped',
        'tasks_zombie', 'pid', 'priority', 'nice', 'parent_pid', 'uid', 'real_uid', 'saved_uid',
        'gid', 'pgrp', 'tty_process_gid', 'session_id', 'thread_count', 'last_used_processor',
        'major_page_fault_count', 'minor_page_fault_count', 'dirty_pages_count', 'thread_gid',
        'major_page_fault_count_delta', 'minor_page_fault_count_delta', 'ipc_namespace_inode',
        'mount_namespace_inode', 'net_namespace_inode', 'pid_namespace_inode',
        'user_namespace_inode', 'nts_namespace_inode', 'numa_node', 'out_of_mem_adjustment',
        'out_of_mem_score', 'resident_anon_mem', 'resident_file_backed_mem', 'resident_locked_mem',
        'resident_shared_mem'
    }

    float_list: Set = {
        'load_1m', 'load_5m', 'load_15m', 'cpu_user', 'cpu_sys', 'cpu_nice', 'cpu_idle', 'cpu_wait',
        'cpu_hardware', 'cpu_software', 'cpu_steal', 'percent_cpu', 'percent_mem', 'mem_total',
        'mem_free', 'mem_used', 'mem_buff_cache', 'swap_total', 'swap_free', 'swap_used',
        'mem_available', 'virtual_mem', 'resident_mem', 'shared_mem', 'swap', 'code', 'data', 'used'
    }

    for idx, item in enumerate(proc_data):
        for key in item:
            # root truncation warnings
            if isinstance(item[key], str) and item[key].endswith('+') and not quiet:
                jc.utils.warning_message([f'item[{idx}]["{key}"] was truncated by top'])

            # root int and float conversions
            if key in int_list:
                item[key] = jc.utils.convert_to_int(item[key])

            if key in float_list:
                item[key] = jc.utils.convert_to_float(item[key])

        for p_idx, proc in enumerate(item['processes']):
            # rename processes keys to conform to schema
            proc_copy = proc.copy()
            for old_key in proc_copy.keys():
                if old_key in proc:
                    proc[key_map[old_key]] = proc.pop(old_key)
                else:
                    jc.utils.warning_message([f'Unknown field detected at item[{idx}]["processes"]: {old_key}'])

            # cleanup values
            for key in proc.keys():

                # set dashes to nulls
                if proc[key] == '-':
                    proc[key] = None

                # because of ambiguous column spacing (right-justified numbers
                # with left-justified dashes for null values) there are some hanging
                # dashes that need to be cleaned up in some values. Seems the correct
                # values are kept in the assigned columns, so this should not affect
                # data integrity.
                if proc[key] and proc[key].endswith(' -'):
                    new_val = proc[key][::-1]
                    new_val = new_val.replace('- ', '')
                    new_val = new_val[::-1]
                    proc[key] = new_val

                # do int/float conversions for the process objects
                if proc[key]:
                    if key in int_list:
                        proc[key] = jc.utils.convert_to_int(proc[key])

                    if key in float_list:
                        proc[key] = jc.utils.convert_to_float(proc[key])

            # set status string
            if proc.get('status'):
                proc['status'] = status_map[proc['status']]

            # split supplementary_gids to a list of integers
            if proc.get('supplementary_gids'):
                proc['supplementary_gids'] = _safe_split(
                    proc['supplementary_gids'],
                    f'item[{idx}]["processes"][{p_idx}]["supplementary_gids"]',
                    ',', quiet=quiet
                )

                proc['supplementary_gids'] = [jc.utils.convert_to_int(x) for x in proc['supplementary_gids']]

            # split supplementary_groups to a list of strings
            if proc.get('supplementary_groups'):
                proc['supplementary_groups'] = _safe_split(
                    proc['supplementary_groups'],
                    f'item[{idx}]["processes"][{p_idx}]["supplementary_groups"]',
                    ',', quiet=quiet
                )

            # split environment_variables to a list of strings
            if proc.get('environment_variables'):
                proc['environment_variables'] = _safe_split(
                    proc['environment_variables'],
                    f'item[{idx}]["processes"][{p_idx}]["environment_variables"]',
                    quiet=quiet
                )

            for key in proc.keys():
                # print final warnings for truncated string values
                if isinstance(proc[key], str) and proc[key].endswith('+') and not quiet:
                    jc.utils.warning_message([f'item[{idx}]["processes"][{p_idx}]["{key}"] was truncated by top'])

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
    item_obj: Dict = {}
    process_table = False
    process_list: List = []

    if jc.utils.has_data(data):

        for line in data.splitlines():
            if line.startswith('top - '):
                if item_obj:
                    if process_list:
                        item_obj['processes'] = parse_table(process_list)
                    raw_output.append(item_obj)
                    process_table = False
                    process_list = []
                    item_obj = {}

                uptime_str = line[6:]
                item_obj.update(parse_uptime(uptime_str, raw=True, quiet=True))
                continue

            if line.startswith('Tasks:'):
                # Tasks: 112 total,   1 running, 111 sleeping,   0 stopped,   0 zombie
                line_list = line.split()
                item_obj.update(
                    {
                        'tasks_total': line_list[1],
                        'tasks_running': line_list[3],
                        'tasks_sleeping': line_list[5],
                        'tasks_stopped': line_list[7],
                        'tasks_zombie': line_list[9]
                    }
                )
                continue

            if line.startswith('%Cpu(s):'):
                # %Cpu(s):  5.9 us,  5.9 sy,  0.0 ni, 88.2 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
                line_list = line.split()
                item_obj.update(
                    {
                        'cpu_user': line_list[1],
                        'cpu_sys': line_list[3],
                        'cpu_nice': line_list[5],
                        'cpu_idle': line_list[7],
                        'cpu_wait': line_list[9],
                        'cpu_hardware': line_list[11],
                        'cpu_software': line_list[13],
                        'cpu_steal': line_list[15]
                    }
                )
                continue

            if line[1:].startswith('iB Mem :'):
                # KiB Mem :  3861332 total,  3446476 free,   216940 used,   197916 buff/cache
                line_list = line.split()
                item_obj.update(
                    {
                        'mem_total': line_list[3],
                        'mem_free': line_list[5],
                        'mem_used': line_list[7],
                        'mem_buff_cache': line_list[9]
                    }
                )
                continue

            if line[1:].startswith('iB Swap:'):
                # KiB Swap:  2097148 total,  2097148 free,        0 used.  3419356 avail Mem
                line_list = line.split()
                item_obj.update(
                    {
                        'swap_total': line_list[2],
                        'swap_free': line_list[4],
                        'swap_used': line_list[6],
                        'mem_available': line_list[8]
                    }
                )
                continue

            if not process_table and line == '':
                process_table = True
                continue

            if process_table and not line == '':
                process_list.append(line)
                continue

        if item_obj:
            if process_list:
                item_obj['processes'] = parse_table(process_list)
            raw_output.append(item_obj)

    return raw_output if raw else _process(raw_output, quiet=quiet)
