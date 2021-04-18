"""jc - JSON CLI output utility `ntpq -p` command output parser

Usage (cli):

    $ ntpq -p | jc --ntpq

    or

    $ jc ntpq -p

Usage (module):

    import jc.parsers.ntpq
    result = jc.parsers.ntpq.parse(ntpq_command_output)

Schema:

    [
      {
        "state":            string,        # space/~ converted to null
        "remote":           string,
        "refid":            string,
        "st":               integer,
        "t":                string,
        "when":             integer,       # - converted to null
        "poll":             integer,
        "reach":            integer,
        "delay":            float,
        "offset":           float,
        "jitter":           float
      },
    ]

Examples:

    $ ntpq -p | jc --ntpq -p
    [
      {
        "remote": "44.190.6.254",
        "refid": "127.67.113.92",
        "st": 2,
        "t": "u",
        "when": 1,
        "poll": 64,
        "reach": 1,
        "delay": 23.399,
        "offset": -2.805,
        "jitter": 2.131,
        "state": null
      },
      {
        "remote": "ntp.wdc1.us.lea",
        "refid": "130.133.1.10",
        "st": 2,
        "t": "u",
        "when": null,
        "poll": 64,
        "reach": 1,
        "delay": 93.053,
        "offset": -0.807,
        "jitter": 2.839,
        "state": null
      },
      {
        "remote": "clock.team-cymr",
        "refid": "204.9.54.119",
        "st": 2,
        "t": "u",
        "when": null,
        "poll": 64,
        "reach": 1,
        "delay": 70.337,
        "offset": -2.909,
        "jitter": 2.6,
        "state": null
      },
      {
        "remote": "mirror1.sjc02.s",
        "refid": "216.218.254.202",
        "st": 2,
        "t": "u",
        "when": 2,
        "poll": 64,
        "reach": 1,
        "delay": 29.325,
        "offset": 1.044,
        "jitter": 4.069,
        "state": null,
      }
    ]

    $ ntpq -pn| jc --ntpq -p
    [
      {
        "remote": "44.190.6.254",
        "refid": "127.67.113.92",
        "st": 2,
        "t": "u",
        "when": 66,
        "poll": 64,
        "reach": 377,
        "delay": 22.69,
        "offset": -0.392,
        "jitter": 2.085,
        "state": "+"
      },
      {
        "remote": "108.59.2.24",
        "refid": "130.133.1.10",
        "st": 2,
        "t": "u",
        "when": 63,
        "poll": 64,
        "reach": 377,
        "delay": 90.805,
        "offset": 2.84,
        "jitter": 1.908,
        "state": "-"
      },
      {
        "remote": "38.229.71.1",
        "refid": "204.9.54.119",
        "st": 2,
        "t": "u",
        "when": 64,
        "poll": 64,
        "reach": 377,
        "delay": 68.699,
        "offset": -0.61,
        "jitter": 2.576,
        "state": "+"
      },
      {
        "remote": "72.5.72.15",
        "refid": "216.218.254.202",
        "st": 2,
        "t": "u",
        "when": 63,
        "poll": 64,
        "reach": 377,
        "delay": 22.654,
        "offset": 0.231,
        "jitter": 1.964,
        "state": "*"
      }
    ]

    $ ntpq -pn| jc --ntpq -p -r
    [
      {
        "s": "+",
        "remote": "44.190.6.254",
        "refid": "127.67.113.92",
        "st": "2",
        "t": "u",
        "when": "66",
        "poll": "64",
        "reach": "377",
        "delay": "22.690",
        "offset": "-0.392",
        "jitter": "2.085"
      },
      {
        "s": "-",
        "remote": "108.59.2.24",
        "refid": "130.133.1.10",
        "st": "2",
        "t": "u",
        "when": "63",
        "poll": "64",
        "reach": "377",
        "delay": "90.805",
        "offset": "2.840",
        "jitter": "1.908"
      },
      {
        "s": "+",
        "remote": "38.229.71.1",
        "refid": "204.9.54.119",
        "st": "2",
        "t": "u",
        "when": "64",
        "poll": "64",
        "reach": "377",
        "delay": "68.699",
        "offset": "-0.610",
        "jitter": "2.576"
      },
      {
        "s": "*",
        "remote": "72.5.72.15",
        "refid": "216.218.254.202",
        "st": "2",
        "t": "u",
        "when": "63",
        "poll": "64",
        "reach": "377",
        "delay": "22.654",
        "offset": "0.231",
        "jitter": "1.964"
      }
    ]
"""
import jc.utils
import jc.parsers.universal


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = '`ntpq -p` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'freebsd']
    magic_commands = ['ntpq']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    for entry in proc_data:

        if entry['s'] == '~':
            entry['s'] = None

        entry['state'] = entry.pop('s')

        int_list = ['st', 'when', 'poll', 'reach']
        float_list = ['delay', 'offset', 'jitter']
        for key in entry:
            if key in int_list:
                entry[key] = jc.utils.convert_to_int(entry[key])
            if key in float_list:
                entry[key] = jc.utils.convert_to_float(entry[key])

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

    cleandata = data.splitlines()
    raw_output = []

    if jc.utils.has_data(data):

        cleandata[0] = 's ' + cleandata[0]
        cleandata[0] = cleandata[0].lower()

        # delete header delimiter
        del cleandata[1]

        # separate first character with a space for easier parsing
        for i, line in list(enumerate(cleandata[1:])):
            if line[0] == ' ':
                # fixup for no-state
                cleandata[i + 1] = '~  ' + line[1:]
            else:
                # fixup - realign columns since we added the 's' column
                cleandata[i + 1] = line[:1] + '  ' + line[1:]

            # fixup for occaisional ip/hostname fields with a space
            cleandata[i + 1] = cleandata[i + 1].replace(' (', '_(')

        raw_output = jc.parsers.universal.simple_table_parse(cleandata)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
