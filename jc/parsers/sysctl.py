"""jc - JSON CLI output utility sysctl -a Parser

Usage:

    specify --sysctl as the first argument if the piped input is coming from sysctl -a

    Note: since sysctl output is not easily parsable only a very simple key/value object
          will be output. An attempt is made to convert obvious integers and floats. If no
          conversion is desired, use the -r (raw) option.

Compatibility:

    'linux', 'darwin', 'freebsd'

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
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['sysctl']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data with the following schema:

        {
          "foo":     string/integer/float,         # best guess based on value
          "bar":     string/integer/float,
          "baz":     string/integer/float
        }
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

    raw_output = {}

    if jc.utils.has_data(data):
        data = data.splitlines()

        # linux uses = and bsd uses :
        if ' = ' in data[0]:
            delim = ' = '
        else:
            delim = ': '

        for line in data:
            linedata = line.split(delim, maxsplit=1)

            # bsd adds values to newlines, which need to be fixed up with this try/except block
            try:
                key = linedata[0]
                value = linedata[1]

                # syctl -a repeats some keys on linux. Append values from repeating keys
                # to the previous key value
                if key in raw_output:
                    existing_value = raw_output[key]
                    raw_output[key] = existing_value + '\n' + value
                    continue

                # fix for weird multiline output in bsd
                # if the key looks strange (has spaces or no dots) then it's probably a value field
                # on a separate line. in this case, just append it to the previous key in the dictionary.
                if '.' not in key or ' ' in key:
                    previous_key = [*raw_output.keys()][-1]
                    raw_output[previous_key] = raw_output[previous_key] + '\n' + line
                    continue

                # if the key looks normal then just add to the dictionary as normal
                else:
                    raw_output[key] = value
                    continue

            # if there is an IndexError exception, then there was no delimiter in the line.
            # In this case just append the data line as a value to the previous key.
            except IndexError:
                prior_key = [*raw_output.keys()][-1]
                raw_output[prior_key] = raw_output[prior_key] + '\n' + line
                continue

    if raw:
        return raw_output
    else:
        return process(raw_output)
