r"""jc - JSON Convert `hash sum` command output parser

This parser works with the following hash calculation utilities:
- `md5`
- `md5sum`
- `shasum`
- `sha1sum`
- `sha224sum`
- `sha256sum`
- `sha384sum`
- `sha512sum`

Usage (cli):

    $ md5sum file.txt | jc --hashsum

or

    $ jc md5sum file.txt

Usage (module):

    import jc
    result = jc.parse('hashsum', md5sum_command_output)

Schema:

    [
      {
        "filename":     string,
        "mode":         string,
        "hash":         string,
      }
    ]

Examples:

    $ md5sum * | jc --hashsum -p
    [
      {
        "filename": "devtoolset-3-gcc-4.9.2-6.el7.x86_64.rpm",
        "mode": "text",
        "hash": "65fc958c1add637ec23c4b137aecf3d3"
      },
      {
        "filename": "digout",
        "mode": "text",
        "hash": "5b9312ee5aff080927753c63a347707d"
      },
      {
        "filename": "dmidecode.out",
        "mode": "text",
        "hash": "716fd11c2ac00db109281f7110b8fb9d"
      },
      {
        "filename": "file with spaces in the name",
        "mode": "text",
        "hash": "d41d8cd98f00b204e9800998ecf8427e"
      },
      {
        "filename": "id-centos.out",
        "mode": "text",
        "hash": "4295be239a14ad77ef3253103de976d2"
      },
      {
        "filename": "ifcfg.json",
        "mode": "text",
        "hash": "01fda0d9ba9a75618b072e64ff512b43"
      },
      ...
    ]
"""
import re
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = 'hashsum command parser (`md5sum`, `shasum`, etc.)'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Parses MD5 and SHA hash program output'
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['md5sum', 'md5', 'shasum', 'sha1sum', 'sha224sum',
                      'sha256sum', 'sha384sum', 'sha512sum']
    tags = ['command']


__version__ = info.version

_mode_friendly_names = {
    " ": "text",
    "*": "binary",
    # Perl shasum -- specific
    "U": "universal",
    "^": "bits",
    # BSD-style format only supports binary mode
    None: "binary"
}

def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """

    for entry in proc_data:
        entry['mode'] = _mode_friendly_names.get(entry['mode'],entry['mode'])

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

        for line in filter(None, data.splitlines()):
            # check for legacy md5 command output
            if line.startswith('MD5 ('):
                file_hash = line.split('=', maxsplit=1)[1].strip()
                file_name = line.split('=', maxsplit=1)[0].strip()
                file_name = file_name[5:]
                file_name = file_name[:-1]
                # filler, legacy md5 always uses binary mode
                file_mode = None
            # standard md5sum and shasum command output
            else:
                m = re.match('([0-9a-f]+) (.)(.*)$', line)
                if not m:
                    raise ValueError(f'Invalid line format: "{line}"')
                file_hash, file_mode, file_name = m.groups()

            item = {
                'filename': file_name,
                'mode': file_mode,
                'hash': file_hash
            }
            raw_output.append(item)

    return raw_output if raw else _process(raw_output)
