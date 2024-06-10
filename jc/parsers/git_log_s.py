r"""jc - JSON Convert `git log` command output streaming parser

> This streaming parser outputs JSON Lines (cli) or returns an Iterable of
> Dictionaries (module)

Can be used with the following format options:
- `oneline`
- `short`
- `medium`
- `full`
- `fuller`

Additional options supported:
- `--stat`
- `--shortstat`

The `epoch` calculated timestamp field is naive. (i.e. based on the
local time of the system the parser is run on)

The `epoch_utc` calculated timestamp field is timezone-aware and is
only available if the timezone field is UTC.

Usage (cli):

    $ git log | jc --git-log-s

Usage (module):

    import jc

    result = jc.parse('git_log_s', git_log_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "commit":               string,
      "author":               string/null,
      "author_email":         string/null,
      "date":                 string,
      "epoch":                integer,  # [0]
      "epoch_utc":            integer,  # [1]
      "commit_by":            string/null,
      "commit_by_email":      string/null,
      "commit_by_date":       string,
      "message":              string,
      "stats" : {
        "files_changed":      integer,
        "insertions":         integer,
        "deletions":          integer,
        "files": [
                              string
        ],
        "file_stats": [
          {
            "name":           string,
            "lines_changed":  integer
          }
        ]
      }

      # below object only exists if using -qq or ignore_exceptions=True
      "_jc_meta": {
        "success":      boolean,     # false if error parsing
        "error":        string,      # exists if "success" is false
        "line":         string       # exists if "success" is false
      }
    }

    [0] naive timestamp if "date" field is parsable, else null
    [1] timezone aware timestamp available for UTC, else null

Examples:

    $ git log | jc --git-log-s
    {"commit":"a730ae18c8e81c5261db132df73cd74f272a0a26","author":"Kelly...}
    {"commit":"930bf439c06c48a952baec05a9896c8d92b7693e","author":"Kelly...}
    ...
"""
import re
from typing import List, Dict, Any, Iterable, Union
import jc.utils
from jc.parsers.git_log import _parse_name_email
from jc.streaming import (
    add_jc_meta, streaming_input_type_check, streaming_line_input_type_check, raise_or_yield
)
from jc.exceptions import ParseError


hash_pattern = re.compile(r'(?:[0-9]|[a-f]){40}')
changes_pattern = re.compile(r'\s(?P<files>\d+)\s+(files? changed)(?:,\s+(?P<insertions>\d+)\s+(insertions?\(\+\)))?(?:,\s+(?P<deletions>\d+)\s+(deletions?\(\-\)))?')


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = '`git log` command streaming parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command']
    streaming = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    int_list = {'files_changed', 'insertions', 'deletions', 'lines_changed'}

    if 'date' in proc_data:
        ts = jc.utils.timestamp(proc_data['date'], format_hint=(1100,))
        proc_data['epoch'] = ts.naive
        proc_data['epoch_utc'] = ts.utc

    if 'stats' in proc_data:
        for key in proc_data['stats']:
            if key in int_list:
                proc_data['stats'][key] = jc.utils.convert_to_int(proc_data['stats'][key])

        if 'file_stats' in proc_data['stats']:
                file_stats = proc_data['stats']['file_stats']
                for file_entry in file_stats:
                    for key in file_entry:
                        if key in int_list:
                            file_entry[key] = jc.utils.convert_to_int(file_entry[key])

    return proc_data


def _is_commit_hash(hash_string: str) -> bool:
    # 0c55240e9da30ac4293dc324f1094de2abd3da91
    if len(hash_string) != 40:
        return False

    if hash_pattern.match(hash_string):
        return True

    return False


@add_jc_meta
def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> Union[Iterable[Dict], tuple]:
    """
    Main text parsing generator function. Returns an iterable object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.splitlines())

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True


    Returns:

        Iterable of Dictionaries
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    streaming_input_type_check(data)

    output_line: Dict = {}
    message_lines: List[str] = []
    file_list: List[str] = []
    file_stats_list: List[Dict[str, Any]] = []

    for line in data:
        try:
            streaming_line_input_type_check(line)

            if line == '' or line == '\n':
                continue

            line_list = line.rstrip().split(maxsplit=1)

            # oneline style
            if not line.startswith(' ') and line_list and _is_commit_hash(line_list[0]):
                if output_line:
                    if file_list:
                        output_line['stats']['files'] = file_list

                    if file_stats_list:
                        output_line['stats']['file_stats'] = file_stats_list

                    yield output_line if raw else _process(output_line)

                    output_line = {}
                    message_lines = []
                    file_list = []
                    file_stats_list = []
                output_line = {
                    'commit': line_list[0],
                    'message': line_list[1]
                }
                continue

            # all other styles
            if line.startswith('commit '):
                if output_line:
                    if message_lines:
                        output_line['message'] = '\n'.join(message_lines)

                    if file_list:
                        output_line['stats']['files'] = file_list

                    if file_stats_list:
                        output_line['stats']['file_stats'] = file_stats_list

                    yield output_line if raw else _process(output_line)

                    output_line = {}
                    message_lines = []
                    file_list = []
                    file_stats_list = []
                output_line['commit'] = line_list[1]
                continue

            if line.startswith('Merge: '):
                output_line['merge'] = line_list[1]
                continue

            if line.startswith('Author: '):
                output_line['author'], output_line['author_email'] = _parse_name_email(line_list[1])
                continue

            if line.startswith('Date: '):
                output_line['date'] = line_list[1]
                continue

            if line.startswith('AuthorDate: '):
                output_line['date'] = line_list[1]
                continue

            if line.startswith('CommitDate: '):
                output_line['commit_by_date'] = line_list[1]
                continue

            if line.startswith('Commit: '):
                output_line['commit_by'], output_line['commit_by_email'] = _parse_name_email(line_list[1])
                continue

            if line.startswith('    '):
                message_lines.append(line.strip())
                continue

            if line.startswith(' ') and 'changed, ' not in line:
                # this is a file name
                file_line_split = line.split('|')
                file_name = file_line_split[0].strip()
                file_list.append(file_name)

                if len(file_line_split) > 1:
                    file_stats = file_line_split[1].strip()
                    lines_changed_str = file_stats.split(' ')
                    lines_changed_count_str = lines_changed_str[0].strip()

                file_stat = {}
                file_stat["name"] = file_name
                file_stat["lines_changed"] = lines_changed_count_str
                file_stats_list.append(file_stat)
                continue

            if line.startswith(' ') and 'changed, ' in line:
                # this is the stat summary
                changes = changes_pattern.match(line)
                if changes:
                    files = changes['files']
                    insertions = changes['insertions']
                    deletions = changes['deletions']

                output_line['stats'] = {
                    'files_changed': files or '0',
                    'insertions': insertions or '0',
                    'deletions':  deletions or '0'
                }
                continue

            raise ParseError('Not git_log_s data')

        except Exception as e:
            yield raise_or_yield(ignore_exceptions, e, line)

    try:
        if output_line:
            if message_lines:
                output_line['message'] = '\n'.join(message_lines)

            if file_list:
                output_line['stats']['files'] = file_list

            if file_stats_list:
                output_line['stats']['file_stats'] = file_stats_list

            yield output_line if raw else _process(output_line)

    except Exception as e:
        yield raise_or_yield(ignore_exceptions, e, line)
