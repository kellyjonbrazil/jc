"""jc - JSON CLI output utility `hash sum` command output parser

Usage (cli):

    $ md5sum | jc --hashsum

    or

    $ jc md5sum file.txt

Usage (module):

    import jc.parsers.hashsum
    result = jc.parsers.hashsum.parse(md5sum_command_output)

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Examples:

    $ md5sum file.txt | jc --hashsum -p
    []
"""
import jc.utils


class info():
    version = '1.0'
    description = 'hashsum command and file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Parses MD5 and SHA hash program output'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['md5sum', 'md5', 'shasum', 'sha1sum', 'sha224sum', 'sha256sum', 'sha384sum', 'sha512sum']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        List of dictionaries. Structured data with the following schema:

        [
          {
            "md5sum":     string,
            "bar":     boolean,
            "baz":     integer
          }
        ]
    """

    # rebuild output for added semantic information
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            # check for legacy md5 command output
            if line.startswith('MD5 ('):
                file_hash = line.split('=')[1].strip()
                file_name = line.split('=')[0].strip()
                file_name = file_name[5:]
                file_name = file_name[:-1]
            # standard md5sum and shasum command output
            else:
                file_hash = line.split()[0]
                file_name = line.split()[1]

            item = {
                'filename': file_name,
                'hash': file_hash
            }
            raw_output.append(item)

    if raw:
        return raw_output
    else:
        return process(raw_output)
