"""jc - JSON CLI output utility w Parser

Usage:

    specify --w as the first argument if the piped input is coming from w

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Examples:

    $ w | jc --w -p
    [
      {
        "user": "root",
        "tty": "tty1",
        "from": null,
        "login_at": "07:49",
        "idle": "1:15m",
        "jcpu": "0.00s",
        "pcpu": "0.00s",
        "what": "-bash"
      },
      {
        "user": "root",
        "tty": "ttyS0",
        "from": null,
        "login_at": "06:24",
        "idle": "0.00s",
        "jcpu": "0.43s",
        "pcpu": "0.00s",
        "what": "w"
      },
      {
        "user": "root",
        "tty": "pts/0",
        "from": "192.168.71.1",
        "login_at": "06:29",
        "idle": "2:35m",
        "jcpu": "0.00s",
        "pcpu": "0.00s",
        "what": "-bash"
      }
    ]

    $ w | jc --w -p -r
    [
      {
        "user": "kbrazil",
        "tty": "tty1",
        "from": "-",
        "login_at": "07:49",
        "idle": "1:16m",
        "jcpu": "0.00s",
        "pcpu": "0.00s",
        "what": "-bash"
      },
      {
        "user": "kbrazil",
        "tty": "ttyS0",
        "from": "-",
        "login_at": "06:24",
        "idle": "2.00s",
        "jcpu": "0.46s",
        "pcpu": "0.00s",
        "what": "w"
      },
      {
        "user": "kbrazil",
        "tty": "pts/0",
        "from": "192.168.71.1",
        "login_at": "06:29",
        "idle": "2:36m",
        "jcpu": "0.00s",
        "pcpu": "0.00s",
        "what": "-bash"
      }
    ]
"""
import string
import jc.utils


class info():
    version = '1.3'
    description = 'w command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['w']


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
            "user":     string,     # '-'' = null
            "tty":      string,     # '-'' = null
            "from":     string,     # '-'' = null
            "login_at": string,     # '-'' = null
            "idle":     string,     # '-'' = null
            "jcpu":     string,
            "pcpu":     string,
            "what":     string      # '-'' = null
          }
        ]
    """
    for entry in proc_data:
        null_list = ['user', 'tty', 'from', 'login_at', 'idle', 'what']
        for key in null_list:
            if key in entry:
                if entry[key] == '-':
                    entry[key] = None

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

    cleandata = data.splitlines()[1:]
    raw_output = []

    if jc.utils.has_data(data):

        header_text = cleandata[0].lower()
        # fixup for 'from' column that can be blank
        from_col = header_text.find('from')
        # clean up 'login@' header
        # even though @ in a key is valid json, it can make things difficult
        header_text = header_text.replace('login@', 'login_at')
        headers = [h for h in ' '.join(header_text.strip().split()).split() if h]

        # parse lines
        raw_output = []
        if cleandata:
            for entry in cleandata[1:]:
                output_line = {}

                # normalize data by inserting Null for missing data
                temp_line = entry.split(maxsplit=len(headers) - 1)

                # fix from column, always at column 2
                if 'from' in headers:
                    if entry[from_col] in string.whitespace:
                        temp_line.insert(2, '-')

                output_line = dict(zip(headers, temp_line))
                raw_output.append(output_line)

        # strip whitespace from beginning and end of all string values
        for row in raw_output:
            for item in row:
                if isinstance(row[item], str):
                    row[item] = row[item].strip()

    if raw:
        return raw_output
    else:
        return process(raw_output)
