"""jc - JSON CLI output utility `file` command output parser

Usage (cli):

    $ file * | jc --file

    or

    $ jc file *

Usage (module):

    import jc.parsers.file
    result = jc.parsers.file.parse(file_command_output)

Schema:

    [
      {
        "filename":   string,
        "type   ":    string
      }
    ]

Examples:

    $ file * | jc --file -p
    [
      {
        "filename": "Applications",
        "type": "directory"
      },
      {
        "filename": "another file with spaces",
        "type": "empty"
      },
      {
        "filename": "argstest.py",
        "type": "Python script text executable, ASCII text"
      },
      {
        "filename": "blkid-p.out",
        "type": "ASCII text"
      },
      {
        "filename": "blkid-pi.out",
        "type": "ASCII text, with very long lines"
      },
      {
        "filename": "cd_catalog.xml",
        "type": "XML 1.0 document text, ASCII text, with CRLF line terminators"
      },
      {
        "filename": "centosserial.sh",
        "type": "Bourne-Again shell script text executable, UTF-8 Unicode text"
      },
      ...
    ]
"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.3'
    description = '`file` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'aix', 'freebsd', 'darwin']
    magic_commands = ['file']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    # No further processing
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

    warned = False

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            linedata = line.rsplit(': ', maxsplit=1)

            try:
                filename = linedata[0].strip()
                filetype = linedata[1].strip()

                raw_output.append(
                    {
                        'filename': filename,
                        'type': filetype
                    }
                )
            except IndexError:
                if not warned:
                    jc.utils.warning_message('Filenames with newline characters detected. Some filenames may be truncated.')
                    warned = True

    if raw:
        return raw_output
    else:
        return _process(raw_output)
