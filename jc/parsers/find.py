"""jc - JSON Convert `find` command output parser

Usage (cli):

    $ find | jc --find

Usage (module):

    import jc
    result = jc.parse('find', find_command_output)

Schema:

    [
      {
        "directory path":           string,
        "file or empty directory:   string
      }
    ]

Examples:

    $ find | jc --find -p
    [
        {
          "directory path": "./directory"
          "file or empty directory": "filename"
        },
        {
          "directory path": "./anotherdirectory"
          "file or empty directory": "anotherfile"
        },
        ...
    ]

    $ find | jc --find -p -r
    {
      "./templates/readme_template",
      "./templates/manpage_template",
      "./.github/workflows/pythonapp.yml",
      ...
    }
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

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """

    processed = []
    for i in proc_data:
        try:
            temp = str(i).rindex("/")
        except ValueError:
            pass
        proc_line = {
            'directory path': i[:temp + 1],
            'file or empty directory': i[temp + 1:]
        }
        
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

        Dictionary of raw structured data or
        List of Dictionaries of processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []
    
    if jc.utils.has_data(data):
        previous = ""
        new_line = data.split("\n")
        for index in new_line:
            if (index[:len(previous)] != previous):
                raw_output.append(previous)
            previous = index
        raw_output.append(previous)

    if raw:
        return raw_output
    else:
        return _process(raw_output)