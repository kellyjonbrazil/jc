r"""jc - JSON Convert `ansible-playbook --list-tags` command output parser

Usage (cli):

    $ ansible-playbook --list-tags playbook.yaml | jc --ansible-playbook-list-tags

or

    $ jc ansible-playbook --list-tags playbook.yaml

Usage (module):

    import jc
    result = jc.parse('ansible_playbook_list_tags', ansible_playbook_command_output)

Schema:

    [
      {
        "playbook":     string,
        "plays": [
          {
            "number":    integer,
            "hosts":     array,
            "name":      string,
            "tags":      array,
            "task_tags": array
          }
        ]
      }
    ]

Examples:

    $ ansible-playbook --list-tags playbook.yaml | jc --ansible-playbook-list-tags -p
    [
      {
        "playbook": "playbook.yaml",
        "plays": [
          {
            "number": 1,
            "hosts": [
              "all"
            ],
            "name": "all",
            "tags": [],
            "task_tags": []
          }
        ]
      }
    ]
"""
import re
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`ansible-playbook --list-tags` command parser'
    author = 'Rahul Ranjan'
    author_email = '11793455+rahul05ranjan@users.noreply.github.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']

    # tags options: generic, standard, file, string, binary, command, slurpable
    tags = ['command']
    magic_commands = ['ansible-playbook --list-tags']

    # other attributes - only enable if needed
    deprecated = False
    hidden = False


__version__ = info.version


_playbook_line = re.compile(r'^playbook:\s*(?P<playbook>.+?)\s*$')
_play_line = re.compile(
    r'^\s*play\s+#(?P<number>\d+)\s+\((?P<pattern>[^)]*)\):\s*'
    r'(?P<name>.*?)\s*TAGS:\s*\[(?P<tags>.*)\]\s*$'
)
_task_tags_line = re.compile(r'^\s*TASK TAGS:\s*\[(?P<task_tags>.*)\]\s*$')


def _split_tags(tag_string: str) -> List[str]:
    """Split a TAGS: / TASK TAGS: list into tag elements."""
    return [tag.strip() for tag in tag_string.split(',') if tag.strip()]


def _split_hosts(pattern: str) -> List[str]:
    """Split a play's host pattern into its host / group selectors."""
    return [host for host in re.split(r'[,:]', pattern) if host]


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for playbook in proc_data:
        for play in playbook['plays']:
            play['number'] = jc.utils.convert_to_int(play['number'])

    return proc_data


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

    if jc.utils.has_data(data):

        current_playbook: Dict = None
        current_play: Dict = None

        for line in data.splitlines():
            stripped = line.strip()

            if not stripped:
                continue

            playbook_match = _playbook_line.match(stripped)
            if playbook_match:
                current_playbook = {
                    'playbook': playbook_match.group('playbook'),
                    'plays': []
                }
                raw_output.append(current_playbook)
                current_play = None
                continue

            task_tags_match = _task_tags_line.match(line)
            if task_tags_match:
                if current_play is not None:
                    current_play['task_tags'] = _split_tags(
                        task_tags_match.group('task_tags')
                    )
                continue

            play_match = _play_line.match(line)
            if play_match:
                number = play_match.group('number')
                pattern = play_match.group('pattern')
                name = play_match.group('name').strip()
                if not name:
                    # ansible uses the host pattern as the play name when
                    # the play has no explicit name
                    name = pattern

                current_play = {
                    'number': number,
                    'hosts': _split_hosts(pattern),
                    'name': name,
                    'tags': _split_tags(play_match.group('tags')),
                    'task_tags': []
                }

                if current_playbook is not None:
                    current_playbook['plays'].append(current_play)
                else:
                    # tolerate play lines that appear before a playbook line
                    current_playbook = {'playbook': None, 'plays': [current_play]}
                    raw_output.append(current_playbook)

                continue

    return raw_output if raw else _process(raw_output)
