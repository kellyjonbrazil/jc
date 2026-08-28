r"""jc - JSON Convert `git diff --name-status` command output parser

Only the `--name-status` output format is currently supported.

Usage (cli):

    $ git diff --name-status | jc --git-diff

or

    $ jc git diff --name-status

Usage (module):

    import jc
    result = jc.parse('git_diff', git_diff_command_output)

Schema:

    [
      {
        "status":       string,        # A, M, D, R, C, T, U, or X
        "similarity":   integer/null,  # [0]
        "old_path":     string/null,   # [0]
        "path":         string
      }
    ]

    [0] only available for renamed (`R`) and copied (`C`) entries

Examples:

    $ git diff --name-status | jc --git-diff -p
    [
      {
        "status": "M",
        "similarity": null,
        "old_path": null,
        "path": "bootstrap/bootstrap.sh"
      },
      {
        "status": "D",
        "similarity": null,
        "old_path": null,
        "path": "configs/sample.json"
      },
      {
        "status": "A",
        "similarity": null,
        "old_path": null,
        "path": "scripts/status.py"
      },
      {
        "status": "R",
        "similarity": 100,
        "old_path": "README.md",
        "path": "README_now.md"
      }
    ]

    $ git diff --name-status | jc --git-diff -p -r
    [
      {
        "status": "R100",
        "similarity": null,
        "old_path": "README.md",
        "path": "README_now.md"
      }
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`git diff --name-status` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['git diff']
    tags = ['command']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    for entry in proc_data:
        entry['status'] = entry['status'][0]
        entry['similarity'] = jc.utils.convert_to_int(entry['similarity'])

    return proc_data


def parse(data, raw=False, quiet=False):
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

    raw_output = []

    if jc.utils.has_data(data):
        for line in data.splitlines():
            if not line.strip():
                continue

            fields = line.split('\t')
            status = fields[0]
            paths = fields[1:]

            entry = {
                'status': status,
                'similarity': None,
                'old_path': None,
                'path': None,
            }

            # renamed (R###) and copied (C###) entries have an old and new path
            if status[0] in ('R', 'C') and len(paths) == 2:
                entry['similarity'] = status[1:]
                entry['old_path'] = paths[0]
                entry['path'] = paths[1]
            elif paths:
                entry['path'] = paths[0]

            raw_output.append(entry)

    return raw_output if raw else _process(raw_output)
