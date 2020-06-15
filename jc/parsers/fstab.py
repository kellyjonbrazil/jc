"""jc - JSON CLI output utility fstab Parser

Usage:

    specify --fstab as the first argument if the piped input is coming from a fstab file

Compatibility:

    'linux', 'freebsd'

Examples:

    $ cat /etc/fstab | jc --fstab -p
    [
      {
        "fs_spec": "/dev/mapper/centos-root",
        "fs_file": "/",
        "fs_vfstype": "xfs",
        "fs_mntops": "defaults",
        "fs_freq": 0,
        "fs_passno": 0
      },
      {
        "fs_spec": "UUID=05d927bb-5875-49e3-ada1-7f46cb31c932",
        "fs_file": "/boot",
        "fs_vfstype": "xfs",
        "fs_mntops": "defaults",
        "fs_freq": 0,
        "fs_passno": 0
      },
      {
        "fs_spec": "/dev/mapper/centos-swap",
        "fs_file": "swap",
        "fs_vfstype": "swap",
        "fs_mntops": "defaults",
        "fs_freq": 0,
        "fs_passno": 0
      }
    ]

    $ cat /etc/fstab | jc --fstab -p -r
    [
      {
        "fs_spec": "/dev/mapper/centos-root",
        "fs_file": "/",
        "fs_vfstype": "xfs",
        "fs_mntops": "defaults",
        "fs_freq": "0",
        "fs_passno": "0"
      },
      {
        "fs_spec": "UUID=05d927bb-5875-49e3-ada1-7f46cb31c932",
        "fs_file": "/boot",
        "fs_vfstype": "xfs",
        "fs_mntops": "defaults",
        "fs_freq": "0",
        "fs_passno": "0"
      },
      {
        "fs_spec": "/dev/mapper/centos-swap",
        "fs_file": "swap",
        "fs_vfstype": "swap",
        "fs_mntops": "defaults",
        "fs_freq": "0",
        "fs_passno": "0"
      }
    ]
"""
import jc.utils


class info():
    version = '1.3'
    description = 'fstab file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'freebsd']


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
            "fs_spec":      string,
            "fs_file":      string,
            "fs_vfstype":   string,
            "fs_mntops":    string,
            "fs_freq":      integer,
            "fs_passno":    integer
          }
        ]
    """
    for entry in proc_data:
        int_list = ['fs_freq', 'fs_passno']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
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

    raw_output = []
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if jc.utils.has_data(data):

        for line in cleandata:
            output_line = {}
            # ignore commented lines
            if line.strip().startswith('#'):
                continue

            line_list = line.split(maxsplit=6)
            fs_spec = line_list[0]
            fs_file = line_list[1]
            fs_vfstype = line_list[2]
            fs_mntops = line_list[3]
            fs_freq = line_list[4]
            fs_passno = line_list[5]

            output_line['fs_spec'] = fs_spec
            output_line['fs_file'] = fs_file
            output_line['fs_vfstype'] = fs_vfstype
            output_line['fs_mntops'] = fs_mntops
            output_line['fs_freq'] = fs_freq
            output_line['fs_passno'] = fs_passno

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
