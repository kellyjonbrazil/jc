r"""jc - JSON Convert `brew search` command output parser

The `brew search` command has no machine-readable output, so this parser reads
the `==> Formulae` and `==> Casks` sections of the default text output.

Usage (cli):

    $ brew search git | jc --brew-search

or

    $ jc brew search git

Usage (module):

    import jc
    result = jc.parse('brew_search', brew_search_command_output)

Schema:

    [
      {
        "name":     string,
        "type":     string    # formula or cask
      }
    ]

Examples:

    $ brew search git | jc --brew-search -p
    [
      {
        "name": "bagit",
        "type": "formula"
      },
      {
        "name": "bash-git-prompt",
        "type": "formula"
      },
      {
        "name": "gitkraken",
        "type": "cask"
      }
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`brew search` command parser'
    author = 'PerryLink'
    author_email = 'novelnexusai@outlook.com'
    compatible = ['darwin', 'linux']
    magic_commands = ['brew search']
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
    # no further processing
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
    section_types = {'formulae': 'formula', 'casks': 'cask'}
    current = None

    if jc.utils.has_data(data):
        for line in jc.utils.splitlines(data):
            line = line.strip()

            if not line:
                continue

            # section header: "==> Formulae" / "==> Casks"
            if line.startswith('==> '):
                current = section_types.get(line[4:].strip().lower())
                continue

            # anything before the first header is not a result line
            if not current:
                continue

            # results are name columns, one or two per line
            for name in line.split():
                raw_output.append({'name': name, 'type': current})

    if raw:
        return raw_output
    else:
        return _process(raw_output)
