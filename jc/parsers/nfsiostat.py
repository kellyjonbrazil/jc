r"""jc - JSON Convert `nfsiostat` command output parser

Parses the per-mount reports printed by `nfsiostat` from `nfs-utils`.

Each report is converted to one object per mount point. When `nfsiostat`
is run with an interval and count (e.g. `nfsiostat 1 5`) the reports are
returned in order as a flat list.

Every RPC operation table in the report (`read` and `write` by default, or
`getattr`, `access`, `lookup`, `readdir`, and `readdirplus` with the `-a`
and `-d` options) is converted to an object named after the operation.
The cache summary lines printed by the `-a`, `-d`, and `-p` options are not
parsed.

The `errors` and `errors_percent` fields are only present when `nfsiostat`
prints the `errors` column, which needs a kernel that reports per-operation
error counts.

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
        "<operation>": {            # read, write, getattr, lookup, etc.
          "ops_s":                  float,
          "kb_s":                   float,
          "kb_op":                  float,
          "retrans":                integer,
          "retrans_percent":        float,
          "avg_rtt_ms":             float,
          "avg_exe_ms":             float,
          "avg_queue_ms":           float,
          "errors":                 integer,
          "errors_percent":         float
        }
      }
    ]

Examples:

    $ nfsiostat /archive | jc --nfsiostat -p
    [
      {
        "filesystem": "192.168.128.220:/mnt/warm/archivedb",
        "mount": "/archive",
        "ops_sec": 4.234,
        "rpc_bklog": 0.0,
        "read": {
          "ops_s": 0.0,
          "kb_s": 0.0,
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
          "ops_s": 0.0,
          "kb_s": 0.0,
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
          "ops_s": "0.000",
          "kb_s": "0.000",
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
          "ops_s": "0.000",
          "kb_s": "0.000",
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
"""
import re
from typing import List, Dict, Optional
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`nfsiostat` command parser'
    author = 'Yang Bai'
    author_email = '271969568+ybai08@users.noreply.github.com'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['nfsiostat']


__version__ = info.version


MOUNT_RE = re.compile(r'^(?P<filesystem>\S.*) mounted on (?P<mount>.+):$')
OP_HEADER_RE = re.compile(r'^(?P<op>[a-z]+):\s+ops/s\s')
COLUMN_SPLIT_RE = re.compile(r'\s{2,}|\t')

COLUMN_KEYS = {
    'ops/s': 'ops_s',
    'kB/s': 'kb_s',
    'kB/op': 'kb_op',
    'retrans': 'retrans',
    'avg RTT (ms)': 'avg_rtt_ms',
    'avg exe (ms)': 'avg_exe_ms',
    'avg queue (ms)': 'avg_queue_ms',
    'errors': 'errors'
}

# columns printed as "count (percent%)"
COUNT_PERCENT_KEYS = {'retrans', 'errors'}


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'retrans', 'errors'}

    for entry in proc_data:
        for key in ('ops_sec', 'rpc_bklog'):
            if key in entry:
                entry[key] = jc.utils.convert_to_float(entry[key])

        for value in entry.values():
            if isinstance(value, dict):
                for key in value:
                    if key in int_list:
                        value[key] = jc.utils.convert_to_int(value[key])
                    else:
                        value[key] = jc.utils.convert_to_float(value[key])

    return proc_data


def _parse_op_values(columns: List[str], line: str) -> Optional[Dict]:
    values = line.split()
    op_stats: Dict = {}

    for column in columns:
        key = COLUMN_KEYS.get(column)
        if key is None or not values:
            return None

        op_stats[key] = values.pop(0)

        if key in COUNT_PERCENT_KEYS:
            if not values:
                return None
            op_stats[key + '_percent'] = values.pop(0).strip('()%')

    return op_stats


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
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

    raw_output: List[Dict] = []
    mount: Dict = {}
    # what the next values line belongs to: 'mount' or an operation name
    section: Optional[str] = None
    columns: List[str] = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            stripped = line.strip()

            if not stripped:
                continue

            mount_match = MOUNT_RE.match(stripped)
            if mount_match:
                mount = {
                    'filesystem': mount_match.group('filesystem'),
                    'mount': mount_match.group('mount')
                }
                raw_output.append(mount)
                section = None
                continue

            if not mount:
                continue

            if stripped.startswith('ops/s') and 'rpc bklog' in stripped:
                section = 'mount'
                continue

            op_match = OP_HEADER_RE.match(stripped)
            if op_match:
                section = op_match.group('op')
                columns = COLUMN_SPLIT_RE.split(stripped.split(':', maxsplit=1)[1].strip())
                continue

            if section == 'mount':
                values = stripped.split()
                if len(values) == 2:
                    mount['ops_sec'], mount['rpc_bklog'] = values
                section = None
                continue

            if section:
                op_stats = _parse_op_values(columns, stripped)
                if op_stats:
                    mount[section] = op_stats
                section = None
                continue

            # anything else (the -a, -d, and -p cache summary lines) is skipped

    return raw_output if raw else _process(raw_output)
