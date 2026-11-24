r"""jc - JSON Convert `nfsiostat` command output streaming parser

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
"""
from typing import Dict, Iterable, List, Optional
import jc.utils
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.jc_types import JSONDictType, StreamingOutputType
from jc.exceptions import ParseError
from jc.parsers.nfsiostat import (
    MOUNT_RE, OP_HEADER_RE, COLUMN_SPLIT_RE, KNOWN_OPS, NO_MOUNTS_MESSAGE, _mount_label, _parse_op_values,
    _process as _process_list
)


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`nfsiostat` command streaming parser'
    author = 'Yang Bai'
    author_email = '271969568+ybai08@users.noreply.github.com'
    compatible = ['linux']
    tags = ['command']
    streaming = True


__version__ = info.version


SKIP = '<skip>'


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    return _process_list([proc_data])[0]


@add_jc_meta
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> StreamingOutputType:
    """
    Main text parsing generator function. Returns an iterable object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.split('\\n'))

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True

    Returns:

        Iterable of Dictionaries
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    streaming_input_type_check(data)

    output_line: Dict = {}
    # what the next values line belongs to: 'mount', an operation name, or
    # SKIP for the values line of an unknown operation table
    section: Optional[str] = None
    columns: List[str] = []

    def warn(message: str) -> None:
        if not quiet:
            jc.utils.warning_message([message])

    def warn_if_values_line_missing() -> None:
        if section is not None:
            warn(f'{_mount_label(output_line["mount"])}: missing the values line after a header line')

    def end_of_mount_block() -> None:
        warn_if_values_line_missing()

        if not any(isinstance(value, dict) for value in output_line.values()):
            warn(f'{_mount_label(output_line["mount"])}: no operation statistics found (truncated input?)')

    for line in data:
        try:
            streaming_line_input_type_check(line)
            stripped = line.strip()

            # skip blank lines
            if not stripped:
                continue

            # a mount header ends the previous mount block, so output it
            mount_match = MOUNT_RE.match(stripped)
            if mount_match:
                if output_line:
                    end_of_mount_block()
                    finished_mount = output_line
                    output_line = {}
                    yield finished_mount if raw else _process(finished_mount)

                output_line = {
                    'filesystem': mount_match.group('filesystem'),
                    'mount': mount_match.group('mount')
                }
                section = None
                continue

            if not output_line:
                if stripped == NO_MOUNTS_MESSAGE:
                    continue
                raise ParseError('Not nfsiostat data')

            if stripped.startswith('ops/s') and 'rpc bklog' in stripped:
                warn_if_values_line_missing()
                if 'ops_sec' in output_line:
                    raise ParseError(f'{_mount_label(output_line["mount"])}: more than one ops/s line in a mount block')
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
                    warn(f'{_mount_label(output_line["mount"])}: skipping unknown operation table: {op}')
                    section = SKIP
                continue

            if section == 'mount':
                section = None
                values = stripped.split()
                if len(values) != 2:
                    raise ParseError(f'{_mount_label(output_line["mount"])}: unexpected number of fields')
                output_line['ops_sec'], output_line['rpc_bklog'] = values
                continue

            if section == SKIP:
                section = None
                continue

            if section:
                op = section
                section = None
                op_stats = _parse_op_values(columns, stripped)
                if not op_stats:
                    raise ParseError(f'{_mount_label(output_line["mount"])}: could not parse {op} values')
                output_line[op] = op_stats
                continue

            # anything else (the -a, -d, and -p cache summary lines) is skipped

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)

    # gather final item
    try:
        if output_line:
            end_of_mount_block()
            yield output_line if raw else _process(output_line)

    except Exception as e:
        yield raise_or_yield(ignore_exceptions, e, '')
