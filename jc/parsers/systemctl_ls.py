"""jc - JSON CLI output utility `systemctl list-sockets` command output parser

Usage (cli):

    $ systemctl list-sockets | jc --systemctl-ls

    or

    $ jc systemctl list-sockets

Usage (module):

    import jc.parsers.systemctl_ls
    result = jc.parsers.systemctl_ls.parse(systemctl_ls_command_output)

Schema:

    [
      {
        "listen":       string,
        "unit":         string,
        "activates":    string
      }
    ]

Examples:

    $ systemctl list-sockets | jc --systemctl-ls -p
    [
      {
        "listen": "/dev/log",
        "unit": "systemd-journald.socket",
        "activates": "systemd-journald.service"
      },
      {
        "listen": "/run/dbus/system_bus_socket",
        "unit": "dbus.socket",
        "activates": "dbus.service"
      },
      {
        "listen": "/run/dmeventd-client",
        "unit": "dm-event.socket",
        "activates": "dm-event.service"
      },
      ...
    ]
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.4'
    description = '`systemctl list-sockets` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['systemctl list-sockets']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data to conform to the schema.
    """
    # nothing more to process
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

    # Clear any blank lines
    linedata = list(filter(None, data.splitlines()))
    raw_output = []

    if jc.utils.has_data(data):

        cleandata = []
        # clean up non-ascii characters, if any
        for entry in linedata:
            cleandata.append(entry.encode('ascii', errors='ignore').decode())

        header_text = cleandata[0].lower()
        header_list = header_text.split()

        raw_output = []

        for entry in cleandata[1:]:
            if 'sockets listed.' in entry:
                break

            else:
                entry_list = entry.rsplit(maxsplit=2)
                output_line = dict(zip(header_list, entry_list))
                raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
