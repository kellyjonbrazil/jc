r"""jc - JSON Convert `upsc` command output parser

Parses the output of the `upsc` command from Network UPS Tools (NUT),
which reports UPS status as simple `key: value` pairs.

An attempt is made to convert values that are obviously numeric (integers
and floats) while leaving identifier-like values (such as serial numbers
or vendor/product IDs that have significant leading zeros) as strings. If
no conversion is desired, use the `-r` command-line argument or the
`raw=True` argument in `parse()`.

Usage (cli):

    $ upsc ups@localhost | jc --upsc

or

    $ jc upsc ups@localhost

Usage (module):

    import jc
    result = jc.parse('upsc', upsc_command_output)

Schema:

    {
      "key1":     string/integer/float,     # best guess based on value
      "key2":     string/integer/float,
      "key3":     string/integer/float
    }

Examples:

    $ upsc ups@localhost | jc --upsc -p
    {
      "battery_charge": 100,
      "battery_voltage": 24.0,
      "device_serial": "000000000000",
      "ups_status": "OL",
      "ups_vendorid": "0764"
      ...
    }

    $ upsc ups@localhost | jc --upsc -p -r
    {
      "battery_charge": "100",
      "battery_voltage": "24.0",
      "device_serial": "000000000000",
      "ups_status": "OL",
      "ups_vendorid": "0764"
      ...
    }
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`upsc` command parser'
    author = 'Mayoka'
    author_email = 'j.mayoka@mayokajohn.com'
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['upsc']
    tags = ['command']


__version__ = info.version


def _safe_numeric(value):
    """
    Convert a string to int or float only if doing so round-trips back
    to the exact same string. This preserves identifier-like values with
    significant leading zeros (e.g. serial numbers, vendor/product IDs)
    as strings while still converting genuine numeric values.
    """
    try:
        as_int = int(value)
        if str(as_int) == value:
            return as_int
    except (ValueError, TypeError):
        pass

    try:
        as_float = float(value)
        if str(as_float) == value:
            return as_float
    except (ValueError, TypeError):
        pass

    return value


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    for key in proc_data:
        proc_data[key] = _safe_numeric(proc_data[key])

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        for line in data.splitlines():
            if not line.strip():
                continue

            key, sep, value = line.partition(': ')
            if not sep:
                continue

            raw_output[key.strip()] = value.strip()

        raw_output = {jc.utils.normalize_key(k): v for k, v in raw_output.items()}

    return raw_output if raw else _process(raw_output)
