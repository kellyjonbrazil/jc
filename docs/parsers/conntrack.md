[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.conntrack"></a>

# jc.parsers.conntrack

jc - JSON Convert `conntrack` command output parser

Parses the `conntrack -L` connection table and the `conntrack -E` event log.
Each line becomes one item: tuple fields keep the names conntrack prints,
prefixed with `orig_` or `reply_`, bracket flags go in `status`, and the
footnotes below mark the fields that depend on the protocol or an output
option.

The `expect`, `dying`, and `unconfirmed` tables and the `-o xml` and `-o save`
output formats are not supported.

Usage (cli):

    $ conntrack -L | jc --conntrack
    $ timeout 10 conntrack -E | jc --conntrack

or

    $ jc conntrack -L

Usage (module):

    import jc
    result = jc.parse('conntrack', conntrack_command_output)

Schema:

    [
      {
        "event":             string/null,   # [0]
        "event_timestamp":   float/null,    # [1]
        "family":            string/null,   # [2]
        "family_number":     integer/null,  # [2]
        "protocol":          string,
        "protocol_number":   integer,
        "timeout":           integer/null,  # [3]
        "state":             string/null,   # [4]
        "status": [
                             string
        ],
        "orig_src":          string,
        "orig_dst":          string,
        "orig_sport":        integer,       # [5]
        "orig_dport":        integer,       # [5]
        "orig_srckey":       integer,       # [6]
        "orig_dstkey":       integer,       # [6]
        "orig_type":         integer,       # [7]
        "orig_code":         integer,       # [7]
        "orig_id":           integer,       # [7]
        "orig_packets":      integer,       # [8]
        "orig_bytes":        integer,       # [8]
        "orig_zone":         integer,       # [9]
        "reply_src":         string,
        "reply_dst":         string,
        "reply_sport":       integer,       # [5]
        "reply_dport":       integer,       # [5]
        "reply_srckey":      integer,       # [6]
        "reply_dstkey":      integer,       # [6]
        "reply_type":        integer,       # [7]
        "reply_code":        integer,       # [7]
        "reply_id":          integer,       # [7]
        "reply_packets":     integer,       # [8]
        "reply_bytes":       integer,       # [8]
        "reply_zone":        integer,       # [9]
        "mark":              integer,
        "use":               integer,
        "zone":              integer,       # [9]
        "secctx":            string,        # [10]
        "secmark":           string,        # [11]
        "helper":            string,        # [12]
        "labels":            string,        # [13]
        "delta_time":        integer,       # [14]
        "start":             string,        # [14]
        "start_epoch":       integer,       # [14]
        "stop":              string,        # [14]
        "stop_epoch":        integer,       # [14]
        "id":                integer,       # [15]
        "portid":            integer,       # [16]
        "progname":          string         # [16]
      }
    ]

    [0] null on `-L` lines, which have no event name; `NEW`, `UPDATE`, or
        `DESTROY` on `-E` lines
    [1] only with `-o timestamp`
    [2] only with `-o extended`; `family` is the layer 3 protocol name and
        `family_number` its number
    [3] null when conntrack does not print it, e.g. on `[DESTROY]` lines
    [4] null for protocols without a state, such as UDP and ICMP
    [5] only for TCP, UDP, UDPLite, SCTP, and DCCP
    [6] only for GRE; converted from hexadecimal
    [7] only for ICMP and ICMPv6
    [8] only with the `net.netfilter.nf_conntrack_acct` sysctl
    [9] `zone` is the flow-wide zone; `orig_zone`/`reply_zone` are the
        per-tuple `zone-orig=`/`zone-reply=` fields, which conntrack prints
        when the zone applies to a single direction
    [10] only when the kernel provides a security context (SELinux)
    [11] only when an SELinux secmark is set
    [12] only when a conntrack helper is attached
    [13] only with `-o labels` and a configured label map
    [14] `delta_time` only with the `net.netfilter.nf_conntrack_timestamp`
         sysctl; `start`/`stop` and their `_epoch` fields additionally
         require `-o ktimestamp`; `_epoch` is a naive local timestamp
    [15] only with `-o id`
    [16] only with `-o userspace` on `-E` events

Examples:

    $ conntrack -L | jc --conntrack -p
    [
      {
        "event": null,
        "event_timestamp": null,
        "family": null,
        "family_number": null,
        "protocol": "tcp",
        "protocol_number": 6,
        "timeout": 115,
        "state": "TIME_WAIT",
        "status": [
          "ASSURED"
        ],
        "orig_src": "10.42.0.18",
        "orig_dst": "192.168.67.80",
        "orig_sport": 34884,
        "orig_dport": 9000,
        "reply_src": "192.168.67.80",
        "reply_dst": "192.168.114.132",
        "reply_sport": 9000,
        "reply_dport": 65479,
        "mark": 0,
        "use": 1
      }
    ]

<a id="jc.parsers.conntrack.parse"></a>

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

Source: [`jc/parsers/conntrack.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/conntrack.py)

Version 1.1 by Tung Lam (53996158+tunglambk@users.noreply.github.com)
