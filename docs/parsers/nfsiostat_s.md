[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.nfsiostat_s"></a>

# jc.parsers.nfsiostat_s

jc - JSON Convert `nfsiostat` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Parses the per-mount reports printed by `nfsiostat` from `nfs-utils`. Use
it with an interval and no count (e.g. `nfsiostat 1`), which runs until it
is stopped.

Each report is converted to one object per mount point. A mount object is
output when the next mount header is read or the input ends, so with an
interval the last mount of each report is output when the next report
starts.

With an interval, the first report for each mount covers the time since
the file system was mounted, and later reports cover each interval.

The cache summary lines printed by the `-a`, `-d`, and `-p` options are not
parsed.

Usage (cli):

    $ nfsiostat 1 | jc --nfsiostat-s

> Note: When piping `jc` converted `nfsiostat` output to other processes it
> may appear the output is hanging due to the OS pipe buffers. This is
> because `nfsiostat` output is too small to quickly fill up the buffer. Use
> the `-u` option to unbuffer the `jc` output if you would like immediate
> output. See the
> [readme](https://github.com/kellyjonbrazil/jc/tree/master#unbuffering-output)
> for more information.

Usage (module):

    import jc

    result = jc.parse('nfsiostat_s', nfsiostat_command_output.split('\n'))
    for item in result:
        # do something

Schema:

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
      },

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":                boolean,    # false if error parsing
        "error":                  string,     # exists if "success" is false
        "line":                   string      # exists if "success" is false
      }
    }

    [0] only with the `-a` option
    [1] only with the `-d` option. `readdirplus` only appears for NFS
        versions that have a READDIRPLUS operation (NFSv3)
    [2] only present when the kernel reports per-operation error counts

Examples:

    $ nfsiostat 1 | jc --nfsiostat-s
    {"filesystem":"192.168.1.10:/export/home","mount":"/home","ops_sec":2.11,...}
    {"filesystem":"nas01.example.com:/volume1/archive","mount":"/mnt/archive",...}
    {"filesystem":"192.168.1.10:/export/home","mount":"/home","ops_sec":1450.0,...}
    ...

    $ nfsiostat 1 | jc --nfsiostat-s -r
    {"filesystem":"192.168.1.10:/export/home","mount":"/home","ops_sec":"2.110",...}
    {"filesystem":"nas01.example.com:/volume1/archive","mount":"/mnt/archive",...}
    {"filesystem":"192.168.1.10:/export/home","mount":"/home","ops_sec":"1450.000",...}
    ...

<a id="jc.parsers.nfsiostat_s.parse"></a>

### parse

```python
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> Iterator[Dict[str, Any] | Tuple[BaseException, str]]
```

Main text parsing generator function. Returns an iterable object.

Parameters:

    data:              (iterable)  line-based text data to parse
                                   (e.g. sys.stdin or str.split('\n'))

    raw:               (boolean)   unprocessed output if True
    quiet:             (boolean)   suppress warning messages if True
    ignore_exceptions: (boolean)   ignore parsing exceptions if True

Returns:

    Iterable of Dictionaries

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/nfsiostat_s.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/nfsiostat_s.py)

Version 1.1 by Yang Bai (271969568+ybai08@users.noreply.github.com)
