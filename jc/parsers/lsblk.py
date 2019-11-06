"""jc - JSON CLI output utility lsblk Parser

Usage:
    specify --lsblk as the first argument if the piped input is coming from lsblk

Limitations:
    the following columns can only be used as the last column:
        HCTL
        LABEL
        MODEL
        MOUNTPOINT
        PARTLABEL
        PARTUUID
        PKNAME
        REV
        SERIAL
        STATE
        SCHED
        TRAN
        UUID
        VENDOR
        WWN

Examples:

$ lsblk -o +STATE | jc --lsblk -p
[
  {
    "name": "sda",
    "maj_min": "8:0",
    "rm": false,
    "size": "20G",
    "ro": false,
    "type": "disk",
    "mountpoint": null,
    "state": "running"
  },
  {
    "name": "sda1",
    "maj_min": "8:1",
    "rm": false,
    "size": "1G",
    "ro": false,
    "type": "part",
    "mountpoint": "/boot"
  },
  {
    "name": "sda2",
    "maj_min": "8:2",
    "rm": false,
    "size": "19G",
    "ro": false,
    "type": "part",
    "mountpoint": null
  },
  {
    "name": "centos-root",
    "maj_min": "253:0",
    "rm": false,
    "size": "17G",
    "ro": false,
    "type": "lvm",
    "mountpoint": "/",
    "state": "running"
  },
  {
    "name": "centos-swap",
    "maj_min": "253:1",
    "rm": false,
    "size": "2G",
    "ro": false,
    "type": "lvm",
    "mountpoint": "[SWAP]",
    "state": "running"
  },
  {
    "name": "sr0",
    "maj_min": "11:0",
    "rm": true,
    "size": "1024M",
    "ro": false,
    "type": "rom",
    "mountpoint": null,
    "state": "running"
  }
]

$ lsblk -o +STATE | jc --lsblk -p -r
[
  {
    "name": "sda",
    "maj_min": "8:0",
    "rm": "0",
    "size": "20G",
    "ro": "0",
    "type": "disk",
    "mountpoint": null,
    "state": "running"
  },
  {
    "name": "sda1",
    "maj_min": "8:1",
    "rm": "0",
    "size": "1G",
    "ro": "0",
    "type": "part",
    "mountpoint": "/boot"
  },
  {
    "name": "sda2",
    "maj_min": "8:2",
    "rm": "0",
    "size": "19G",
    "ro": "0",
    "type": "part",
    "mountpoint": null
  },
  {
    "name": "centos-root",
    "maj_min": "253:0",
    "rm": "0",
    "size": "17G",
    "ro": "0",
    "type": "lvm",
    "mountpoint": "/",
    "state": "running"
  },
  {
    "name": "centos-swap",
    "maj_min": "253:1",
    "rm": "0",
    "size": "2G",
    "ro": "0",
    "type": "lvm",
    "mountpoint": "[SWAP]",
    "state": "running"
  },
  {
    "name": "sr0",
    "maj_min": "11:0",
    "rm": "1",
    "size": "1024M",
    "ro": "0",
    "type": "rom",
    "mountpoint": null,
    "state": "running"
  }
]
"""
import string
import jc


def process(proc_data):
    '''schema:
    [
      {
        "name":         string,
        "maj_min":      string,
        "rm":           boolean,
        "size":         string,
        "ro":           boolean,
        "type":         string,
        "mountpoint":   string,
        "kname":        string,
        "fstype":       string,
        "label":        string,
        "uuid":         string,
        "partlabel":    string,
        "partuuid":     string,
        "ra":           boolean,
        "model":        string,
        "serial":       string,
        "state":        string,
        "owner":        string,
        "group":        string,
        "mode":         string,
        "alignment":    integer,
        "min_io":       integer,
        "opt_io":       integer,
        "phy_sec":      integer,
        "log_sec":      integer,
        "rota":         boolean,
        "sched":        string,
        "rq_size":      integer,
        "disc_aln":     integer,
        "disc_gran":    string,
        "disc_max":     string,
        "disc_zero":    boolean,
        "wsame":        string,
        "wwn":          string,
        "rand":         boolean,
        "pkname":       string,
        "hctl":         string
      }
    ]
    '''
    for entry in proc_data:
        # boolean changes
        bool_list = ['rm', 'ro', 'ra', 'rota', 'disc_zero', 'rand']
        for key in bool_list:
            if key in entry:
                try:
                    key_bool = bool(int(entry[key]))
                    entry[key] = key_bool
                except (ValueError):
                    entry[key] = None

        # integer changes
        int_list = ['alignment', 'min_io', 'opt_io', 'phy_sec', 'log_sec', 'rq_size', 'disc_aln']
        for key in int_list:
            if key in entry:
                try:
                    key_int = int(entry[key])
                    entry[key] = key_int
                except (ValueError):
                    entry[key] = None

    return proc_data


def parse(data, raw=False):
    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    jc.jc.compatibility(__name__,
                        ['linux'])

    raw_output = []
    linedata = data.splitlines()
    # Clear any blank lines
    cleandata = list(filter(None, linedata))
    cleandata = data.splitlines()

    fix_headers = cleandata.pop(0).lower()
    fix_headers = fix_headers.replace('maj:min', 'maj_min')
    fix_headers = fix_headers.replace('-', '_')

    # find mountpoint starting column for fixup
    mpt_col = fix_headers.find('mountpoint')

    headers = fix_headers.split()

    # parse lines
    if cleandata:
        for entry in cleandata:
            output_line = {}

            # normalize data by inserting Null for missing data
            temp_line = entry.split(maxsplit=len(headers) - 1)

            # fix mountpoint column, always at column 6
            if len(entry) > mpt_col:
                if entry[mpt_col] in string.whitespace:
                    temp_line.insert(6, None)

            output_line = dict(zip(headers, temp_line))
            raw_output.append(output_line)

        for entry in raw_output:
            entry['name'] = entry['name'].encode('ascii', errors='ignore').decode()

    if raw:
        return raw_output
    else:
        return process(raw_output)
