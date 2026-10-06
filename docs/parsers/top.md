[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.top"></a>

# jc.parsers.top

jc - JSON Convert `top -b` command output parser

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
        "mem_unit":                                     string,
        "mem_total":                                    float,
        "mem_free":                                     float,
        "mem_used":                                     float,
        "mem_buff_cache":                               float,
        "swap_unit":                                    string,
        "swap_total":                                   float,
        "swap_free":                                    float,
        "swap_used":                                    float,
        "mem_available":                                float,
        "processes": [
          {
            "pid":                                      integer,
            "user":                                     string,
            "priority":                                 integer,
            "nice":                                     integer,
            "virtual_mem":                              float,
            "virtual_mem_bytes":                        integer,
            "virtual_mem_unit":                         string,
            "resident_mem":                             float,
            "resident_mem_bytes":                       integer,
            "resident_mem_unit":                        string,
            "shared_mem":                               float,
            "shared_mem_bytes":                         integer,
            "shared_mem_unit":                          string,
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
            "swap":                                     float,
            "swap_bytes":                               integer,
            "swap_unit":                                string,
            "code":                                     float,
            "code_bytes":                               integer,
            "code_unit":                                string,
            "data":                                     float,
            "data_bytes":                               integer,
            "data_unit":                                string,
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
            "used":                                     float,
            "used_bytes":                               integer,
            "used_unit":                                string,
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

<a id="jc.parsers.top.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/top.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/top.py)

Version 1.3 by Kelly Brazil (kellyjonbrazil@gmail.com)
