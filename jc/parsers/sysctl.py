"""jc - JSON CLI output utility sysctl -a Parser

Usage:

    specify --sysctl as the first argument if the piped input is coming from sysctl -a

    Note: since sysctl output is not easily parsable only a very simple key/value object
          will be output. An attempt is made to covert obvious integers. If no conversion
          is desired, use the -r (raw) option in jc.

Compatibility:

    'linux', 'darwin', 'aix', 'freebsd'

Examples:

    $ sysctl | jc --sysctl -p
    {
      "user.cs_path": "/usr/bin:/bin:/usr/sbin:/sbin",
      "user.bc_base_max": 99,
      "user.bc_dim_max": 2048,
      "user.bc_scale_max": 99,
      "user.bc_string_max": 1000,
      "user.coll_weights_max": 2,
      "user.expr_nest_max": 32
      ...
    }

    $ sysctl | jc --sysctl -p -r
    {
      "user.cs_path": "/usr/bin:/bin:/usr/sbin:/sbin",
      "user.bc_base_max": "99",
      "user.bc_dim_max": "2048",
      "user.bc_scale_max": "99",
      "user.bc_string_max": "1000",
      "user.coll_weights_max": "2",
      "user.expr_nest_max": "32",
      ...
    }
"""
import jc.utils


class info():
    version = '1.0'
    description = 'sysctl command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'aix', 'freebsd']
    magic_commands = ['sysctl']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data with the following schema:

        [
          {
            "foo":     string/integer,
            "bar":     string/integer,
            "baz":     string/integer
          }
        ]
    """
    for key in proc_data:
        try:
            proc_data[key] = int(proc_data[key])
        except (ValueError):
            try:
                proc_data[key] = float(proc_data[key])
            except (ValueError):
                pass
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    tail = 0
    raw_output = {}

    if jc.utils.has_data(data):
        data = data.splitlines()

        # linux uses = and bsd uses :
        if ' = ' in data[0]:
            delim = ' = '
        else:
            delim = ':'

        for line in filter(None, data):
            linedata = line.split(delim, maxsplit=1)
            key = linedata[0]
            value = linedata[1].lstrip()

            # syctl -a repeats some keys on linux. need to make new keys unique if
            # they already exist so we don't lose data.
            if key in raw_output:
                tail += 1
                key = f'{key}_{tail}'
                raw_output[key] = value
            else:
                tail = 0
                raw_output[key] = value

    if raw:
        return raw_output
    else:
        return process(raw_output)
