[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.nfsiostat"></a>

# jc.parsers.nfsiostat

jc - JSON Convert `nfsiostat` command output parser

Parses the per-mount reports printed by `nfsiostat` from `nfs-utils`.

Each report is converted to one object per mount point. When `nfsiostat`
is run with an interval and count (e.g. `nfsiostat 1 5`) the reports are
returned in order as a flat list.

With an interval, the first report for each mount covers the time since
the file system was mounted, and later reports cover each interval.

The cache summary lines printed by the `-a`, `-d`, and `-p` options are not
parsed.

Usage (cli):

    $ nfsiostat | jc --nfsiostat

or

    $ jc nfsiostat

Usage (module):

    import jc
    result = jc.parse('nfsiostat', nfsiostat_command_output)

Schema:

    [
      {
        "filesystem":               string,
        "mount":                    string,
        "ops_sec":                  float,
        "rpc_bklog":                float,
        "read": {
          "ops_sec":                float,
          "kb_sec":                 float,
          "kb_op":                  float,
          "retrans":                integer,
          "retrans_percent":        float,
          "avg_rtt_ms":             float,
          "avg_exe_ms":             float,
          "avg_queue_ms":           float,
          "errors":                 integer,    # [2]
          "errors_percent":         float       # [2]
        },
        "write": {
          "ops_sec":                float,
          "kb_sec":                 float,
          "kb_op":                  float,
          "retrans":                integer,
          "retrans_percent":        float,
          "avg_rtt_ms":             float,
          "avg_exe_ms":             float,
          "avg_queue_ms":           float,
          "errors":                 integer,    # [2]
          "errors_percent":         float       # [2]
        },
        "getattr": {                # [0]
          "ops_sec":                float,
          "kb_sec":                 float,
          "kb_op":                  float,
          "retrans":                integer,
          "retrans_percent":        float,
          "avg_rtt_ms":             float,
          "avg_exe_ms":             float,
          "avg_queue_ms":           float,
          "errors":                 integer,    # [2]
          "errors_percent":         float       # [2]
        },
        "access": {                 # [0]
          "ops_sec":                float,
          "kb_sec":                 float,
          "kb_op":                  float,
          "retrans":                integer,
          "retrans_percent":        float,
          "avg_rtt_ms":             float,
          "avg_exe_ms":             float,
          "avg_queue_ms":           float,
          "errors":                 integer,    # [2]
          "errors_percent":         float       # [2]
        },
        "lookup": {                 # [1]
          "ops_sec":                float,
          "kb_sec":                 float,
          "kb_op":                  float,
          "retrans":                integer,
          "retrans_percent":        float,
          "avg_rtt_ms":             float,
          "avg_exe_ms":             float,
          "avg_queue_ms":           float,
          "errors":                 integer,    # [2]
          "errors_percent":         float       # [2]
        },
        "readdir": {                # [1]
          "ops_sec":                float,
          "kb_sec":                 float,
          "kb_op":                  float,
          "retrans":                integer,
          "retrans_percent":        float,
          "avg_rtt_ms":             float,
          "avg_exe_ms":             float,
          "avg_queue_ms":           float,
          "errors":                 integer,    # [2]
          "errors_percent":         float       # [2]
        },
        "readdirplus": {            # [1]
          "ops_sec":                float,
          "kb_sec":                 float,
          "kb_op":                  float,
          "retrans":                integer,
          "retrans_percent":        float,
          "avg_rtt_ms":             float,
          "avg_exe_ms":             float,
          "avg_queue_ms":           float,
          "errors":                 integer,    # [2]
          "errors_percent":         float       # [2]
        }
      }
    ]

    [0] only with the `-a` option
    [1] only with the `-d` option. `readdirplus` only appears for NFS
        versions that have a READDIRPLUS operation (NFSv3)
    [2] only present when the kernel reports per-operation error counts

Examples:

    $ nfsiostat /archive | jc --nfsiostat -p
    [
      {
        "filesystem": "192.168.128.220:/mnt/warm/archivedb",
        "mount": "/archive",
        "ops_sec": 4.234,
        "rpc_bklog": 0.0,
        "read": {
          "ops_sec": 0.0,
          "kb_sec": 0.0,
          "kb_op": 0.335,
          "retrans": 0,
          "retrans_percent": 0.0,
          "avg_rtt_ms": 6.013,
          "avg_exe_ms": 6.239,
          "avg_queue_ms": 0.013,
          "errors": 0,
          "errors_percent": 0.0
        },
        "write": {
          "ops_sec": 0.0,
          "kb_sec": 0.0,
          "kb_op": 0.0,
          "retrans": 0,
          "retrans_percent": 0.0,
          "avg_rtt_ms": 0.0,
          "avg_exe_ms": 0.0,
          "avg_queue_ms": 0.0,
          "errors": 0,
          "errors_percent": 0.0
        }
      }
    ]

    $ nfsiostat /archive | jc --nfsiostat -p -r
    [
      {
        "filesystem": "192.168.128.220:/mnt/warm/archivedb",
        "mount": "/archive",
        "ops_sec": "4.234",
        "rpc_bklog": "0.000",
        "read": {
          "ops_sec": "0.000",
          "kb_sec": "0.000",
          "kb_op": "0.335",
          "retrans": "0",
          "retrans_percent": "0.0",
          "avg_rtt_ms": "6.013",
          "avg_exe_ms": "6.239",
          "avg_queue_ms": "0.013",
          "errors": "0",
          "errors_percent": "0.0"
        },
        "write": {
          "ops_sec": "0.000",
          "kb_sec": "0.000",
          "kb_op": "0.000",
          "retrans": "0",
          "retrans_percent": "0.0",
          "avg_rtt_ms": "0.000",
          "avg_exe_ms": "0.000",
          "avg_queue_ms": "0.000",
          "errors": "0",
          "errors_percent": "0.0"
        }
      }
    ]

<a id="jc.parsers.nfsiostat.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
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

Source: [`jc/parsers/nfsiostat.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/nfsiostat.py)

Version 1.2 by Yang Bai (271969568+ybai08@users.noreply.github.com)
