"""jc - JSON Convert `git ls-remote` command output parser

This parser outputs two schemas:

- Default: A single object with key/value pairs
- Raw: An array of objects (`--raw` (cli) or `raw=True (module))

See the Schema section for more details

Usage (cli):

    $ git ls-remote | jc --git-ls-remote

or

    $ jc git ls-remote

Usage (module):

    import jc
    result = jc.parse('git_ls_remote', git_ls_remote_command_output)

Schema:

    Default:
    {
      <reference>:            string
    }

    Raw:
    [
      {
        "reference":          string,
        "commit":             string
      }
    ]

Examples:

    $ git ls-remote | jc --git-ls-remote -p
    {
      "HEAD": "214cd6b9e09603b3c4fa02203b24fb2bc3d4e338",
      "refs/heads/dev": "b884f6aacca39e05994596d8fdfa7e7c4f1e0389",
      "refs/heads/master": "214cd6b9e09603b3c4fa02203b24fb2bc3d4e338",
      "refs/pull/1/head": "e416c77bed1267254da972b0f95b7ff1d43fccef",
      ...
    }

    $ git ls-remote | jc --git-ls-remote -p -r
    [
      {
        "reference": "HEAD",
        "commit": "214cd6b9e09603b3c4fa02203b24fb2bc3d4e338"
      },
      {
        "reference": "refs/heads/dev",
        "commit": "b884f6aacca39e05994596d8fdfa7e7c4f1e0389"
      },
      ...
    ]
"""
from typing import List, Union
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`git ls-remote` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['git ls-remote']
    tags = ['command']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    new_dict: JSONDictType = {}

    for item in proc_data:
        new_dict.update(
            {
                item['reference']: item['commit']
            }
        )

    return new_dict


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Union[JSONDictType, List[JSONDictType]]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary (default) or List of Dictionaries (raw)
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[JSONDictType] = []
    output_line: JSONDictType = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            commit, reference = line.split()
            output_line = {
                'reference': reference,
                'commit': commit
            }
            raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
