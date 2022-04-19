"""jc - JSON Convert `git log` command output parser

<<Short git-log description and caveats>>

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
        "git-log":     string,
        "bar":     boolean,
        "baz":     integer
      }
    ]

Examples:

    $ git-log | jc --git-log -p
    []

    $ git-log | jc --git-log -p -r
    []
"""
import re
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`git log` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['git log']


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float, bool
    # conversions and timestamps

    return proc_data


def _is_commit_hash(hash_string: str) -> bool:
    # 0c55240e9da30ac4293cc324f1094de2abd3da91
    if len(hash_string) != 40:
        return False

    hash_pattern = r'([0-9]|[a-f])+'
    if re.match(hash_pattern, hash_string):
        return True

    return False


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
    output_line = {}
    message_lines = []

    if jc.utils.has_data(data):

        for line in data.splitlines():
            line_list = line.split(maxsplit=1)

            # oneline style
            if line_list and _is_commit_hash(line_list[0]):
                output_line = {
                    'commit': line_list[0],
                    'message': line_list[1]
                }
                raw_output.append(output_line)
                continue

            # all other styles
            if line.startswith('commit '):
                if output_line:
                    if message_lines:
                        output_line['message'] = '\n'.join(message_lines)
                    raw_output.append(output_line)
                    output_line = {}
                    message_lines = []
                output_line['commit'] = line_list[1]
                continue

            if line.startswith('Merge: '):
                output_line['merge'] = line_list[1]
                continue

            if line.startswith('Author: '):
                values = line_list[1].rsplit(maxsplit=1)
                output_line['author'] = values[0]
                output_line['author_email'] = values[1].strip('<').strip('>')
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
                values = line_list[1].rsplit(maxsplit=1)
                output_line['commit_by'] = values[0]
                output_line['commit_by_email'] = values[1].strip('<').strip('>')
                continue

            if line.startswith('    '):
                message_lines.append(line.strip())


    if output_line:
        if message_lines:
            output_line['message'] = '\n'.join(message_lines)
        raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
