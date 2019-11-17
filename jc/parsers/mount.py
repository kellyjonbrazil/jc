"""jc - JSON CLI output utility mount Parser

Usage:
    specify --mount as the first argument if the piped input is coming from mount

Example:

    $ mount | jc --mount -p
    [
      {
        "filesystem": "sysfs",
        "mount_point": "/sys",
        "type": "sysfs",
        "access": [
          "rw",
          "nosuid",
          "nodev",
          "noexec",
          "relatime"
        ]
      },
      {
        "filesystem": "proc",
        "mount_point": "/proc",
        "type": "proc",
        "access": [
          "rw",
          "nosuid",
          "nodev",
          "noexec",
          "relatime"
        ]
      },
      {
        "filesystem": "udev",
        "mount_point": "/dev",
        "type": "devtmpfs",
        "access": [
          "rw",
          "nosuid",
          "relatime",
          "size=977500k",
          "nr_inodes=244375",
          "mode=755"
        ]
      },
      ...
    ]
"""
import jc.utils


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        dictionary   structured data with the following schema:
    
        [
          {
            "filesystem":   string,
            "mount_point":  string,
            "type":         string,
            "access": [
                            string
            ]
          }
        ]
    """
    # nothing to process
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        dictionary   raw or processed structured data
    """

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    raw_output = []

    linedata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, linedata))

    if cleandata:
        for entry in cleandata:
            output_line = {}
            parsed_line = entry.split()

            output_line['filesystem'] = parsed_line[0]
            output_line['mount_point'] = parsed_line[2]
            output_line['type'] = parsed_line[4]

            access = parsed_line[5].lstrip('(').rstrip(')').split(',')

            output_line['options'] = access

            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
