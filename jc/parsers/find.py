"""jc - JSON Convert `find` command output parser

This parser returns a list of objects by default and a list of strings if
the `--raw` option is used.

Usage (cli):

    $ find | jc --find

Usage (module):

    import jc
    result = jc.parse('find', find_command_output)

Schema:

    [
      {
        "path":     string,
        "node":     string,
        "error":    string
      }
    ]

Examples:

    $ find | jc --find -p
    [
        {
          "path": "./directory"
          "node": "filename"
        },
        {
          "path": "./anotherdirectory"
          "node": "anotherfile"
        },
        {
          "path":   null
          "node":   null
          "error":  "find: './inaccessible': Permission denied"
        }
        ...
    ]

    $ find | jc --find -p -r
    [
      "./templates/readme_template",
      "./templates/manpage_template",
      "./.github/workflows/pythonapp.yml",
      ...
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`find` command parser'
    author = 'Solomon Leang'
    author_email = 'solomonleang@gmail.com'
    compatible = ['linux']
    tags = ['command']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data: (List of Strings) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    processed = []

    for index in proc_data:
        path, node, error = "", "", ""

        if index == ".":
            node = "."
        elif index.startswith('find: '):
            error = index
        else:
            try:
                path, node = index.rsplit('/', maxsplit=1)
            except ValueError:
                pass

        proc_line = {
            'path': path if path else None,
            'node': node if node else None
        }

        if error:
            proc_line.update(
                {'error': error}
            )

        processed.append(proc_line)

    return processed


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of raw strings or
        List of Dictionaries of processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []

    if jc.utils.has_data(data):
        raw_output = data.splitlines()

    if raw:
        return raw_output
    else:
        return _process(raw_output)