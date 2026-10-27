r"""jc - JSON Convert `nfsiostat` command output parser

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
"""
import re
from typing import List, Dict, Optional
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`nfsiostat` command parser'
    author = 'Yang Bai'
    author_email = '271969568+ybai08@users.noreply.github.com'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['nfsiostat']


__version__ = info.version


MOUNT_RE = re.compile(r'^(?P<filesystem>[^ \t]+) mounted on (?P<mount>.+):$')
OP_HEADER_RE = re.compile(r'^(?P<op>[a-z]+):\s+ops/s\s')
COLUMN_SPLIT_RE = re.compile(r'\s{2,}|\t')

SKIP = '<skip>'
MAX_LABEL_LEN = 256
NO_MOUNTS_MESSAGE = 'No NFS mount points were found'
KNOWN_OPS = {'read', 'write', 'getattr', 'access', 'lookup', 'readdir', 'readdirplus'}

COLUMN_KEYS = {
    'ops/s': 'ops_sec',
    'kB/s': 'kb_sec',
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


def _mount_label(mount_name: str) -> str:
    """Shorten a very long mount point name for use in warning messages."""
    if len(mount_name) > MAX_LABEL_LEN:
        return mount_name[:MAX_LABEL_LEN] + '...'

    return mount_name


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
    # what the next values line belongs to: 'mount', an operation name, or
    # SKIP for the values line of an unknown operation table
    section: Optional[str] = None
    columns: List[str] = []

    def warn(message: str) -> None:
        if not quiet:
            jc.utils.warning_message([message])

    def warn_if_values_line_missing() -> None:
        if section is not None:
            warn(f'{_mount_label(mount["mount"])}: missing the values line after a header line')

    def end_of_mount_block() -> None:
        if not mount:
            return

        warn_if_values_line_missing()

        if not any(isinstance(value, dict) for value in mount.values()):
            warn(f'{_mount_label(mount["mount"])}: no operation statistics found (truncated input?)')

    if jc.utils.has_data(data):

        for line in jc.utils.splitlines(data):
            stripped = line.strip()

            if not stripped:
                continue

            mount_match = MOUNT_RE.match(stripped)
            if mount_match:
                end_of_mount_block()
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
                warn_if_values_line_missing()
                if 'ops_sec' in mount:
                    warn(f'{_mount_label(mount["mount"])}: more than one ops/s line in a mount block')
                section = 'mount'
                continue

            op_match = OP_HEADER_RE.match(stripped)
            if op_match:
                warn_if_values_line_missing()
                op = op_match.group('op')
                if op in KNOWN_OPS:
                    section = op
                    columns = COLUMN_SPLIT_RE.split(stripped.split(':', maxsplit=1)[1].strip())
                else:
                    warn(f'{_mount_label(mount["mount"])}: skipping unknown operation table: {op}')
                    section = SKIP
                continue

            if section == 'mount':
                values = stripped.split()
                if len(values) == 2:
                    mount['ops_sec'], mount['rpc_bklog'] = values
                else:
                    warn(f'{_mount_label(mount["mount"])}: unexpected number of fields: {stripped}')
                section = None
                continue

            if section == SKIP:
                section = None
                continue

            if section:
                op_stats = _parse_op_values(columns, stripped)
                if op_stats:
                    mount[section] = op_stats
                else:
                    warn(f'{_mount_label(mount["mount"])}: could not parse {section} values: {stripped}')
                section = None
                continue

            # anything else (the -a, -d, and -p cache summary lines) is skipped

        end_of_mount_block()

        if not raw_output and NO_MOUNTS_MESSAGE not in data:
            warn('No NFS mount blocks found')

    return raw_output if raw else _process(raw_output)
