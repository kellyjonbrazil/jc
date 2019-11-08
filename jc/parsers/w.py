"""jc - JSON CLI output utility w Parser

Usage:
    specify --w as the first argument if the piped input is coming from w

Example:

$ w | jc --w -p
[
  {
    "user": "root",
    "tty": "ttyS0",
    "from": "-",
    "login_at": "Mon20",
    "idle": "0.00s",
    "jcpu": "14.70s",
    "pcpu": "0.00s",
    "what": "bash"
  },
  {
    "user": "root",
    "tty": "pts/0",
    "from": "192.168.71.1",
    "login_at": "Thu22",
    "idle": "22:46m",
    "jcpu": "0.05s",
    "pcpu": "0.05s",
    "what": "-bash"
  }
]
"""
import string
import jc.utils


def process(proc_data):
    '''schema:
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
    '''
    for entry in proc_data:
        null_list = ['user', 'tty', 'from', 'login_at', 'idle', 'what']
        for key in null_list:
            if key in entry:
                if entry[key] == '-':
                    entry[key] = None

    return proc_data


def parse(data, raw=False, quiet=False):
    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    cleandata = data.splitlines()[1:]
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

    if raw:
        return raw_output
    else:
        return process(raw_output)
