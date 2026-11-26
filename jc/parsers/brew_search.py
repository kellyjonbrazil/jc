r"""jc - JSON Convert `brew search` command output parser

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
        "type":     string/null
      }
    ]

Examples:

    $ brew search git | jc --brew-search -p
    [
      {
        "name": "atomgit-cli",
        "type": "formula"
      },
      {
        "name": "bagit",
        "type": "formula"
      },
      {
        "name": "bash-git-prompt",
        "type": "formula"
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

    if jc.utils.has_data(data):
        lines = jc.utils.splitlines(data)

        # `brew search` only prints the "==> Formulae" / "==> Casks" headers
        # when stdout is a TTY, and jc normally reads a pipe.
        if any(line.strip().startswith('==> ') for line in lines):
            current = None

            for line in lines:
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
                    # installed packages are marked with a trailing check mark
                    # in TTY output (e.g. "git ✔"); it is not part of the name
                    if name == '✔':
                        continue

                    raw_output.append({'name': name, 'type': current})
        else:
            # Piped output: bare names, one per line. A single blank line
            # separates the formulae block from the cask block, and is only
            # printed when both kinds matched (formulae first, then casks).
            blocks = []
            block = []

            for line in lines:
                line = line.strip()

                if line:
                    block.append(line)
                elif block:
                    blocks.append(block)
                    block = []

            if block:
                blocks.append(block)

            # With two blocks the types are known by position. With one block
            # the output does not say which kind it is, so set `type` to null.
            if len(blocks) == 2:
                kinds = ['formula', 'cask']
            else:
                kinds = [None] * len(blocks)

            for block, kind in zip(blocks, kinds):
                for name in block:
                    raw_output.append({'name': name, 'type': kind})

    if raw:
        return raw_output
    else:
        return _process(raw_output)
