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
"""
import shlex
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
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

    if jc.utils.has_data(data):

        split_line = shlex.split(data)

        for item in split_line:
            if '=' in item:
                key, val = item.split('=', maxsplit=1)
                raw_output[key] = val

            else:
                options.append(item)

    if options:
        raw_output['_options'] = options

    return raw_output if raw else _process(raw_output)
