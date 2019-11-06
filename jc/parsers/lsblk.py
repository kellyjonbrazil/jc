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

Example:

$ lsblk | jc --lsblk -p
[
  {
    "name": "sda",
    "maj_min": "8:0",
    "rm": "0",
    "size": "20G",
    "ro": "0",
    "type": "disk"
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
    "type": "part"
  },
  {
    "name": "centos-root",
    "maj_min": "253:0",
    "rm": "0",
    "size": "17G",
    "ro": "0",
    "type": "lvm",
    "mountpoint": "/"
  },
  {
    "name": "centos-swap",
    "maj_min": "253:1",
    "rm": "0",
    "size": "2G",
    "ro": "0",
    "type": "lvm",
    "mountpoint": "[SWAP]"
  },
  {
    "name": "sr0",
    "maj_min": "11:0",
    "rm": "1",
    "size": "1024M",
    "ro": "0",
    "type": "rom"
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
        "min-io":       integer,
        "opt-io":       integer,
        "phy-sec":      integer,
        "log-sec":      integer,
        "rota":         boolean,
        "sched":        string,
        "rq-size":      integer,
        "disc-aln":     integer,
        "disc-gran":    string,
        "disc-max":     string,
        "disc-zero":    boolean,
        "wsame":        string,
        "wwn":          string,
        "rand":         boolean,
        "pkname":       string,
        "hctl":         string
      }
    ]
    '''
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

    if raw:
        return raw_output
    else:
        return process(raw_output)
