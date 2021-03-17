"""jc - JSON CLI output utility `upower` command output parser

<<Short upower description and caveats>>

Usage (cli):

    $ upower | jc --upower

    or

    $ jc upower

Usage (module):

    import jc.parsers.upower
    result = jc.parsers.upower.parse(upower_command_output)

Compatibility:

    'linux'

Examples:

    $ upower | jc --upower -p
    []

    $ upower | jc --upower -p -r
    []
"""
import jc.utils


class info():
    version = '1.0'
    description = 'upower command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['upower']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data with the following schema:

        [
          {
            "upower":     string,
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

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    device_obj = {}
    device_name = None
    detail_obj = {}
    detail_key = ''
    # last_detail_key = ''

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            if line.startswith('Device:') or line.startswith('Daemon:'):
                if device_obj:
                    if detail_obj:
                        device_obj[detail_key] = detail_obj

                    raw_output.append(device_obj)
                    device_obj = {}

                if line.startswith('Device:'):
                    device_name = line.split(':', maxsplit=1)[1].strip()
                    device_obj = {
                        'type': 'Device',
                        "device_name": device_name
                    }

                elif line.startswith('Daemon:'):
                    device_obj = {
                        'type': 'Daemon'
                    }

                detail_obj = {}
                detail_key = ''
                continue

            # history detail lines
            # if detail_key.startswith('history_'):
            if line.startswith('    ') and ':' not in line:
                continue
            #     detail_obj['history_line'] = 'history detail line'
            #     continue

            # general detail lines
            if line.startswith('    ') and ':' in line:
                # since there could be multiple detail objects, reset the object key
                # if detail_key != last_detail_key:
                #     device_obj[last_detail_key] = detail_obj
                #     last_detail_key = detail_key

                key = line.split(':', maxsplit=1)[0].strip().lower().replace('-', '_').replace(' ', '_')
                val = line.split(':', maxsplit=1)[1].strip()
                detail_obj[key] = val
                continue

            # history lines are a special case of detail lines
            # set the history detail key
            if line.startswith('  ') and ':' in line and line.strip().split(':', maxsplit=1)[1] == '':
                continue
            #     detail_key = line.strip().lower().replace('-', '_').replace(' ', '_').replace('(', '').replace(')', '')[:-1]
            #     device_obj[detail_key] = {}
            #     continue

            # top level lines
            if line.startswith('  ') and ':' in line:
                key = line.split(':', maxsplit=1)[0].strip().lower().replace('-', '_').replace(' ', '_')
                val = line.split(':', maxsplit=1)[1].strip()
                device_obj[key] = val
                continue

            # set the detail key
            if line.startswith('  ') and ':' not in line:
                detail_key = line.strip().lower().replace('-', '_').replace(' ', '_')
                device_obj[detail_key] = {}
                continue

    if device_obj:
        if detail_obj:
            device_obj[detail_key] = detail_obj
        raw_output.append(device_obj)

    if raw:
        return raw_output
    else:
        return process(raw_output)
