r"""jc - JSON Convert `git log` command output parser

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

    $ git log | jc --git-log

or

    $ jc git log

Usage (module):

    import jc
    result = jc.parse('git_log', git_log_command_output)

Schema:

    [
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
      }
    ]

    [0] naive timestamp if "date" field is parsable, else null
    [1] timezone aware timestamp available for UTC, else null

Examples:

    $ git log --stat | jc --git-log -p
    [
      {
        "commit": "728d882ed007b3c8b785018874a0eb06e1143b66",
        "author": "Kelly Brazil",
        "author_email": "kellyjonbrazil@gmail.com",
        "date": "Wed Apr 20 09:50:19 2022 -0400",
        "stats": {
          "files_changed": 2,
          "insertions": 90,
          "deletions": 12,
          "files": [
            "docs/parsers/git_log.md",
            "jc/parsers/git_log.py"
          ],
          "file_stats": [
            {
              "name": "docs/parsers/git_log.md",
              "lines_changed": 3
            },
            {
              "name": "jc/parsers/git_log.py",
              "lines_changed": 7
            }
          ]
        },
        "message": "add timestamp docs and examples",
        "epoch": 1650462619,
        "epoch_utc": null
      },
      {
        "commit": "b53e42aca623181aa9bc72194e6eeef1e9a3a237",
        "author": "Kelly Brazil",
        "author_email": "kellyjonbrazil@gmail.com",
        "date": "Wed Apr 20 09:44:42 2022 -0400",
        "stats": {
          "files_changed": 5,
          "insertions": 29,
          "deletions": 6,
          "files": [
            "docs/parsers/git_log.md",
            "docs/utils.md",
            "jc/parsers/git_log.py",
            "jc/utils.py",
            "man/jc.1"
          ],
          "file_stats": [
            {
              "name": "docs/parsers/git_log.md",
              "lines_changed": 3
            },
            {
              "name": "docs/utils.md",
              "lines_changed": 7
            },
            {
              "name": "jc/parsers/git_log.py",
              "lines_changed": 1
            },
            {
              "name": "jc/utils.py",
              "lines_changed": 12
            },
            {
              "name": "man/jc.1",
              "lines_changed": 14
            }
          ]
        },
        "message": "add calculated timestamp",
        "epoch": 1650462282,
        "epoch_utc": null
      },
      ...
    ]

    $ git log --stat | jc --git-log -p -r
    [
      {
        "commit": "728d882ed007b3c8b785018874a0eb06e1143b66",
        "author": "Kelly Brazil",
        "author_email": "kellyjonbrazil@gmail.com",
        "date": "Wed Apr 20 09:50:19 2022 -0400",
        "stats": {
          "files_changed": "2",
          "insertions": "90",
          "deletions": "12",
          "files": [
            "docs/parsers/git_log.md",
            "jc/parsers/git_log.py"
          ],
          "file_stats": [
            {
              "name": "docs/parsers/git_log.md",
              "lines_changed": "3"
            },
            {
              "name": "jc/parsers/git_log.py",
              "lines_changed": "7"
            }
          ]
        },
        "message": "add timestamp docs and examples"
      },
      {
        "commit": "b53e42aca623181aa9bc72194e6eeef1e9a3a237",
        "author": "Kelly Brazil",
        "author_email": "kellyjonbrazil@gmail.com",
        "date": "Wed Apr 20 09:44:42 2022 -0400",
        "stats": {
          "files_changed": "5",
          "insertions": "29",
          "deletions": "6",
          "files": [
            "docs/parsers/git_log.md",
            "docs/utils.md",
            "jc/parsers/git_log.py",
            "jc/utils.py",
            "man/jc.1"
          ],
          "file_stats": [
            {
              "name": "docs/parsers/git_log.md",
              "lines_changed": "3"
            },
            {
              "name": "docs/utils.md",
              "lines_changed": "7"
            },
            {
              "name": "jc/parsers/git_log.py",
              "lines_changed": "1"
            },
            {
              "name": "jc/utils.py",
              "lines_changed": "12"
            },
            {
              "name": "man/jc.1",
              "lines_changed": "14"
            }
          ]
        },
        "message": "add calculated timestamp"
      },
      ...
    ]
"""
import re
from typing import List, Dict, Any
import jc.utils

hash_pattern = re.compile(r'(?:[0-9]|[a-f]){40}')
changes_pattern = re.compile(r'\s(?P<files>\d+)\s+(files? changed)(?:,\s+(?P<insertions>\d+)\s+(insertions?\(\+\)))?(?:,\s+(?P<deletions>\d+)\s+(deletions?\(\-\)))?')

class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = '`git log` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['git log']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list = {'files_changed', 'insertions', 'deletions', 'lines_changed'}

    for entry in proc_data:
        if 'date' in entry:
            ts = jc.utils.timestamp(entry['date'], format_hint=(1100,))
            entry['epoch'] = ts.naive
            entry['epoch_utc'] = ts.utc

        if 'stats' in entry:
            for key in entry['stats']:
                if key in int_list:
                    entry['stats'][key] = jc.utils.convert_to_int(entry['stats'][key])

            if 'file_stats' in entry['stats']:
                file_stats = entry['stats']['file_stats']
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

def _parse_name_email(line):
    values = line.rsplit(maxsplit=1)
    name = None
    email = None

    if len(values) == 2:
        name = values[0]
        if values[1].startswith('<') and values[1].endswith('>'):
            email = values[1][1:-1]
    else:
        if values[0].lstrip().startswith('<') and values[0].endswith('>'):
            email = values[0].lstrip()[1:-1]
        else:
            name = values[0]

    if not name:
        name = None
    if not email:
        email = None # covers '<>' case turning into null, not ''

    return name, email


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
    output_line: Dict = {}
    message_lines: List[str] = []
    file_list: List[str] = []
    file_stats_list: List[Dict[str, Any]] = []

    if jc.utils.has_data(data):

        for line in data.splitlines():
            line_list = line.split(maxsplit=1)

            # oneline style
            if not line.startswith(' ') and line_list and _is_commit_hash(line_list[0]):
                if output_line:
                    if file_list:
                        output_line['stats']['files'] = file_list

                    if file_stats_list:
                        output_line['stats']['file_stats'] = file_stats_list

                    raw_output.append(output_line)
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

                    raw_output.append(output_line)
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

    if output_line:
        if message_lines:
            output_line['message'] = '\n'.join(message_lines)

        if file_list:
            output_line['stats']['files'] = file_list

        if file_stats_list:
            output_line['stats']['file_stats'] = file_stats_list

        raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
