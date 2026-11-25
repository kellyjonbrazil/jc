r"""jc - JSON Convert `/proc/cmdline` file parser

Usage (cli):

    $ cat /proc/cmdline | jc --proc

or

    $ jc /proc/cmdline

or

    $ cat /proc/cmdline | jc --proc-cmdline

Usage (module):

    import jc
    result = jc.parse('proc_cmdline', proc_cmdline_file)

Schema:

    {
      "<key>":          string,
      "_options": [
                        string
      ],
      "_repeated": {
        "<key>": [
                        string
        ]
      },
      "_init_args": [
                        string
      ]
    }

Examples:

    $ cat /proc/cmdline | jc --proc -p
    {
      "BOOT_IMAGE": "clonezilla/live/vmlinuz",
      "consoleblank": "0",
      "keyboard-options": "grp:ctrl_shift_toggle,lctrl_shift_toggle",
      "ethdevice-timeout": "130",
      "toram": "filesystem.squashfs",
      "boot": "live",
      "edd": "on",
      "ocs_daemonon": "ssh lighttpd",
      "ocs_live_run": "sudo screen /usr/sbin/ocs-sr -g auto -e1 auto -e2 -batch -r -j2 -k -scr -p true restoreparts win7-64 sda1",
      "ocs_live_extra_param": "",
      "keyboard-layouts": "us,ru",
      "ocs_live_batch": "no",
      "locales": "ru_RU.UTF-8",
      "vga": "788",
      "net.ifnames": "0",
      "union": "overlay",
      "fetch": "http://10.1.1.1/tftpboot/clonezilla/live/filesystem.squashfs",
      "ocs_postrun99": "sudo reboot",
      "initrd": "clonezilla/live/initrd.img",
      "_options": [
        "config",
        "noswap",
        "nolocales",
        "nomodeset",
        "noprompt",
        "nosplash",
        "nodmraid",
        "components"
      ]
    }

    $ cat /proc/cmdline | jc --proc -p
    {
      "BOOT_IMAGE": "/vmlinuz",
      "root": "/dev/sda1",
      "console": "ttyS0",
      "_options": [
        "ro"
      ],
      "_repeated": {
        "console": [
          "tty0",
          "ttyS0"
        ]
      },
      "_init_args": [
        "single"
      ]
    }
"""
from typing import List, Dict, Tuple, Optional
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`/proc/cmdline` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    return proc_data


_SPACE = ' \t\n\v\f\r'
_RESERVED = ('_options', '_repeated', '_init_args')


def _next_args(data: str) -> List[Tuple[str, Optional[str]]]:
    """
    Split the command line into (parameter, value) pairs the way the kernel
    does in next_arg() (lib/cmdline.c): whitespace separates parameters
    unless it is inside double quotes. There is no escape character and
    single quotes are ordinary characters. A quote that is not closed runs
    to the end of the line. Only the quote around a whole parameter or
    around a value is removed. The value is None if there is no '=' sign.
    A leading '=' is part of the parameter name.
    """
    args: List[Tuple[str, Optional[str]]] = []

    # the trailing newline is added by /proc and is not part of the line
    if data.endswith('\n'):
        data = data[:-1]

    length = len(data)
    pos = 0

    while True:
        while pos < length and data[pos] in _SPACE:
            pos += 1

        if pos >= length:
            break

        quoted = False
        in_quote = False

        if data[pos] == '"':
            pos += 1
            in_quote = True
            quoted = True

        start = pos
        equals = 0
        i = pos

        while i < length:
            char = data[i]
            if char in _SPACE and not in_quote:
                break
            if equals == 0 and char == '=' and i > start:
                equals = i
            if char == '"':
                in_quote = not in_quote
            i += 1

        end = i
        param = data[start:end]
        val: Optional[str] = None

        if equals:
            param = data[start:equals]
            val_start = equals + 1
            val_end = end
            stripped = False

            if val_start < end and data[val_start] == '"':
                val_start += 1
                if data[end - 1] == '"':
                    val_end = max(end - 1, val_start)
                    stripped = True

            if quoted and not stripped and data[end - 1] == '"':
                val_end = max(end - 1, val_start)

            val = data[val_start:val_end]

        elif quoted and end > start and data[end - 1] == '"':
            param = data[start:end - 1]

        # an empty name (lone quote) is a valid parameter for the kernel
        args.append((param, val))

        pos = end

    return args


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> JSONDictType:
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

    raw_output: Dict = {}
    options: List = []
    init_args: List = []
    values: Dict = {}
    in_init = False

    if jc.utils.has_data(data):

        for key, val in _next_args(data):
            if in_init:
                if val is None and key == '--':
                    break
                init_args.append(key if val is None else key + '=' + val)

            elif val is None and key == '--':
                in_init = True

            elif val is None:
                options.append(key)

            elif key in _RESERVED:
                options.append(key + '=' + val)

            else:
                raw_output[key] = val
                values.setdefault(key, []).append(val)

    if options:
        raw_output['_options'] = options

    repeated = {k: v for k, v in values.items() if len(v) > 1}
    if repeated:
        raw_output['_repeated'] = repeated

    if in_init:
        raw_output['_init_args'] = init_args

    return raw_output if raw else _process(raw_output)
