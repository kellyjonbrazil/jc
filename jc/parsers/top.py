"""jc - JSON Convert `top` command output parser

Requires batch mode (`-b`). The `-n` option should also be used to limit
the number of times `top` is run.

Usage (cli):

    $ top -b -n 3 | jc --top

    or

    $ jc top -b -n 3

Usage (module):

    import jc
    result = jc.parse('top', top_command_output)

Schema:

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
        "mem_total":                                    integer,
        "mem_free":                                     integer,
        "mem_used":                                     integer,
        "mem_buff_cache":                               integer,
        "swap_total":                                   integer,
        "swap_free":                                    integer,
        "swap_used":                                    integer,
        "mem_available":                                integer,
        "processes": [
          {
            "pid":                                      integer,
            "user":                                     string,
            "priority":                                 integer,
            "nice":                                     integer,
            "virtual_mem":                              string,
            "resident_mem":                             string,
            "shared_mem":                               string,
            "status":                                   string,
            "percent_cpu":                              float,
            "percent_mem":                              float,
            "time_hundredths ":                         string,
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
            "swap":                                     string,
            "code":                                     string,
            "data":                                     string,
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
            "used":                                     string,
            "ipc_namespace_inode":                      integer,
            "mount_namespace_inode":                    integer,
            "net_namespace_inode":                      integer,
            "pid_namespace_inode":                      integer,
            "user_namespace_inode":                     integer,
            "nts_namespace_inode":                      integer
          }
        ]
      }
    ]

Examples:

    $ top -b -n 3 | jc --top -p
    []

    $ top -b -n 3 | jc --top -p -r
    []
"""
from typing import List, Dict
import jc.utils
from jc.parsers.uptime import parse as parse_uptime
from jc.parsers.universal import sparse_table_parse as parse_table


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`top -b` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['top -b']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
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
        'CGROUPS': 'cgroups',
        'CODE': 'code',
        'COMMAND': 'command',
        'DATA': 'data',
        'Flags': 'flags',
        'GID': 'gid',
        'GROUP': 'group',
        'PGRP': 'pgrp',
        'PID': 'pid',
        'SWAP': 'swap',
        'TIME': 'time',
        'TIME+': 'time_hundredths ',
        'TTY': 'tty',
        'UID': 'uid',
        'USED': 'used',
        'USER': 'user',
        'PR': 'priority',
        'NI': 'nice',
        'VIRT': 'virtual_mem',
        'RES': 'resident_mem',
        'SHR': 'shared_mem',
        'S': 'status',
        'ENVIRON': 'environment_variables',
        'P': 'last_used_processor',
        'PPID': 'parent_pid',
        'RUID': 'real_uid',
        'RUSER': 'real_user',
        'SID': 'session_id',
        'SUID': 'saved_uid',
        'SUPGIDS': 'supplementary_gids',
        'SUPGRPS': 'supplementary_groups',
        'SUSER': 'saved_user',
        'TGID': 'thread_gid',
        'TPGID': 'tty_process_gid',
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
        'R': 'running',
        'S': 'sleeping',
        'T': 'stopped by job control signal',
        't': 'stopped by debugger during trace',
        'Z': 'zombie'
    }

    int_list: List = [
        'uptime',
        'users',
        'tasks_total',
        'tasks_running',
        'tasks_sleeping',
        'tasks_stopped',
        'tasks_zombie',
        'mem_total',
        'mem_free',
        'mem_used',
        'mem_buff_cache',
        'swap_total',
        'swap_free',
        'swap_used',
        'mem_available'
    ]

    float_list: List = [
        'load_1m',
        'load_5m',
        'load_15m',
        'cpu_user',
        'cpu_sys',
        'cpu_nice',
        'cpu_idle',
        'cpu_wait',
        'cpu_hardware',
        'cpu_software',
        'cpu_steal'
    ]


    for item in proc_data:
        # root int and float conversions
        for key in item:
            if key in int_list:
                item[key] = jc.utils.convert_to_int(item[key])

            if key in float_list:
                item[key] = jc.utils.convert_to_float(item[key])

        for proc in item['processes']:
            # rename processes keys to conform to schema
            proc_copy = proc.copy()
            for old_key in proc_copy.keys():
                proc[key_map[old_key]] = proc.pop(old_key)

            # set dashes to nulls
            for key in proc.keys():
                if proc[key] == '-':
                    proc[key] = None

            # set status string
            if proc.get('status'):
                proc['status'] = status_map[proc['status']]

            # split supplementary_gids to a list of integers

            # split supplementary_groups to a list of strings

            # split environment_variables to a list of strings
            if proc.get('environment_variables'):
                env_list = proc['environment_variables'].split()
                env_list = [x if '=' in x else f'{x} (truncated)' for x in env_list]
                proc['environment_variables'] = env_list

            



        

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

        for line in filter(None, data.splitlines()):
            if line.startswith('top - '):
                if item_obj:
                    if process_list:
                        item_obj['processes'] = parse_table(process_list)
                    raw_output.append(item_obj)
                    process_table = False
                    process_list = []
                    item_obj = {}

                uptime_str = line[6:]
                item_obj.update(parse_uptime(uptime_str, raw=True))
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

            if line.startswith('KiB Mem :'):
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

            if line.startswith('   PID '):
                # line = normalize_headers(line)
                process_table = True
                process_list.append(line)
                continue

            if process_table:
                process_list.append(line)
                continue

        if item_obj:
            if process_list:
                item_obj['processes'] = parse_table(process_list)
            raw_output.append(item_obj)

    return raw_output if raw else _process(raw_output)
