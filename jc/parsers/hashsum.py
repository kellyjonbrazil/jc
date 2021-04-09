"""jc - JSON CLI output utility `hash sum` command output parser

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

    import jc.parsers.hashsum
    result = jc.parsers.hashsum.parse(md5sum_command_output)

Schema:

    [
      {
        "filename":     string,
        "hash":         string,
      }
    ]

Examples:

    $ md5sum * | jc --hashsum -p
    [
      {
        "filename": "devtoolset-3-gcc-4.9.2-6.el7.x86_64.rpm",
        "hash": "65fc958c1add637ec23c4b137aecf3d3"
      },
      {
        "filename": "digout",
        "hash": "5b9312ee5aff080927753c63a347707d"
      },
      {
        "filename": "dmidecode.out",
        "hash": "716fd11c2ac00db109281f7110b8fb9d"
      },
      {
        "filename": "file with spaces in the name",
        "hash": "d41d8cd98f00b204e9800998ecf8427e"
      },
      {
        "filename": "id-centos.out",
        "hash": "4295be239a14ad77ef3253103de976d2"
      },
      {
        "filename": "ifcfg.json",
        "hash": "01fda0d9ba9a75618b072e64ff512b43"
      },
      ...
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = 'hashsum command parser (`md5sum`, `shasum`, etc.)'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Parses MD5 and SHA hash program output'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['md5sum', 'md5', 'shasum', 'sha1sum', 'sha224sum', 'sha256sum', 'sha384sum', 'sha512sum']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """

    # no further processing for this parser
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            # check for legacy md5 command output
            if line.startswith('MD5 ('):
                file_hash = line.split('=', maxsplit=1)[1].strip()
                file_name = line.split('=', maxsplit=1)[0].strip()
                file_name = file_name[5:]
                file_name = file_name[:-1]
            # standard md5sum and shasum command output
            else:
                file_hash = line.split(maxsplit=1)[0]
                file_name = line.split(maxsplit=1)[1]

            item = {
                'filename': file_name,
                'hash': file_hash
            }
            raw_output.append(item)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
