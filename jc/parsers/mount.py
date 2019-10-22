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


def parse(data):
    output = []

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

            output_line['access'] = access

            output.append(output_line)

    return output
