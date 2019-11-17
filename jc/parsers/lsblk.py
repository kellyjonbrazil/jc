"""jc - JSON CLI output utility lsblk Parser

Usage:
    specify --lsblk as the first argument if the piped input is coming from lsblk

Examples:

    $ lsblk | jc --lsblk -p
    [
      {
        "name": "sda",
        "maj_min": "8:0",
        "rm": false,
        "size": "20G",
        "ro": false,
        "type": "disk",
        "mountpoint": null
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
      ...
    ]

    $ lsblk -o +KNAME,FSTYPE,LABEL,UUID,PARTLABEL,PARTUUID,RA,MODEL,SERIAL,STATE,OWNER,GROUP,MODE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,DISC-ALN,DISC-GRAN,DISC-MAX,DISC-ZERO,WSAME,WWN,RAND,PKNAME,HCTL,TRAN,REV,VENDOR | jc --lsblk -p
    [
      {
        "name": "sda",
        "maj_min": "8:0",
        "rm": false,
        "size": "20G",
        "ro": false,
        "type": "disk",
        "mountpoint": null,
        "kname": "sda",
        "fstype": null,
        "label": null,
        "uuid": null,
        "partlabel": null,
        "partuuid": null,
        "ra": 4096,
        "model": "VMware Virtual S",
        "serial": null,
        "state": "running",
        "owner": "root",
        "group": "disk",
        "mode": "brw-rw----",
        "alignment": 0,
        "min_io": 512,
        "opt_io": 0,
        "phy_sec": 512,
        "log_sec": 512,
        "rota": true,
        "sched": "deadline",
        "rq_size": 128,
        "disc_aln": 0,
        "disc_gran": "0B",
        "disc_max": "0B",
        "disc_zero": false,
        "wsame": "32M",
        "wwn": null,
        "rand": true,
        "pkname": null,
        "hctl": "0:0:0:0",
        "tran": "spi",
        "rev": "1.0",
        "vendor": "VMware,"
      },
      {
        "name": "sda1",
        "maj_min": "8:1",
        "rm": false,
        "size": "1G",
        "ro": false,
        "type": "part",
        "mountpoint": "/boot",
        "kname": "sda1",
        "fstype": "xfs",
        "label": null,
        "uuid": "05d927bb-5875-49e3-ada1-7f46cb31c932",
        "partlabel": null,
        "partuuid": null,
        "ra": 4096,
        "model": null,
        "serial": null,
        "state": null,
        "owner": "root",
        "group": "disk",
        "mode": "brw-rw----",
        "alignment": 0,
        "min_io": 512,
        "opt_io": 0,
        "phy_sec": 512,
        "log_sec": 512,
        "rota": true,
        "sched": "deadline",
        "rq_size": 128,
        "disc_aln": 0,
        "disc_gran": "0B",
        "disc_max": "0B",
        "disc_zero": false,
        "wsame": "32M",
        "wwn": null,
        "rand": true,
        "pkname": "sda",
        "hctl": null,
        "tran": null,
        "rev": null,
        "vendor": null
      },
      ...
    ]

    $ lsblk -o +KNAME,FSTYPE,LABEL,UUID,PARTLABEL,PARTUUID,RA,MODEL,SERIAL,STATE,OWNER,GROUP,MODE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,DISC-ALN,DISC-GRAN,DISC-MAX,DISC-ZERO,WSAME,WWN,RAND,PKNAME,HCTL,TRAN,REV,VENDOR | jc --lsblk -p -r
    [
      {
        "name": "sda",
        "maj_min": "8:0",
        "rm": "0",
        "size": "20G",
        "ro": "0",
        "type": "disk",
        "mountpoint": null,
        "kname": "sda",
        "fstype": null,
        "label": null,
        "uuid": null,
        "partlabel": null,
        "partuuid": null,
        "ra": "4096",
        "model": "VMware Virtual S",
        "serial": null,
        "state": "running",
        "owner": "root",
        "group": "disk",
        "mode": "brw-rw----",
        "alignment": "0",
        "min_io": "512",
        "opt_io": "0",
        "phy_sec": "512",
        "log_sec": "512",
        "rota": "1",
        "sched": "deadline",
        "rq_size": "128",
        "disc_aln": "0",
        "disc_gran": "0B",
        "disc_max": "0B",
        "disc_zero": "0",
        "wsame": "32M",
        "wwn": null,
        "rand": "1",
        "pkname": null,
        "hctl": "0:0:0:0",
        "tran": "spi",
        "rev": "1.0",
        "vendor": "VMware,"
      },
      {
        "name": "sda1",
        "maj_min": "8:1",
        "rm": "0",
        "size": "1G",
        "ro": "0",
        "type": "part",
        "mountpoint": "/boot",
        "kname": "sda1",
        "fstype": "xfs",
        "label": null,
        "uuid": "05d927bb-5875-49e3-ada1-7f46cb31c932",
        "partlabel": null,
        "partuuid": null,
        "ra": "4096",
        "model": null,
        "serial": null,
        "state": null,
        "owner": "root",
        "group": "disk",
        "mode": "brw-rw----",
        "alignment": "0",
        "min_io": "512",
        "opt_io": "0",
        "phy_sec": "512",
        "log_sec": "512",
        "rota": "1",
        "sched": "deadline",
        "rq_size": "128",
        "disc_aln": "0",
        "disc_gran": "0B",
        "disc_max": "0B",
        "disc_zero": "0",
        "wsame": "32M",
        "wwn": null,
        "rand": "1",
        "pkname": "sda",
        "hctl": null,
        "tran": null,
        "rev": null,
        "vendor": null
      },
      ...
    ]
"""
import string
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
            "ra":           integer,
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
            "hctl":         string,
            "tran":         string,
            "rev":          string,
            "vendor":       string
          }
        ]
    """
    for entry in proc_data:
        # boolean changes
        bool_list = ['rm', 'ro', 'rota', 'disc_zero', 'rand']
        for key in bool_list:
            if key in entry:
                try:
                    key_bool = bool(int(entry[key]))
                    entry[key] = key_bool
                except (ValueError):
                    entry[key] = None

        # integer changes
        int_list = ['ra', 'alignment', 'min_io', 'opt_io', 'phy_sec', 'log_sec', 'rq_size', 'disc_aln']
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

        dictionary   raw or processed structured data
    """

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    # unicode \u2063 = invisible separator and should not be seen in lsblk output
    delim = '\u2063'

    raw_output = []
    linedata = data.splitlines()
    # Clear any blank lines
    cleandata = list(filter(None, linedata))
    cleandata = data.splitlines()

    header_text = cleandata.pop(0).lower()
    header_text = header_text.replace(':', '_')
    header_text = header_text.replace('-', '_')
    header_text = header_text + ' '

    header_list = header_text.split()

    # find each column index and end position
    header_search = [header_list[0]]
    for h in header_list[1:]:
        header_search.append(' ' + h + ' ')

    header_spec_list = []
    for i, column in enumerate(header_list[0:len(header_list) - 1]):
        header_spec = {
            'name': column,
            'end': header_text.find(header_search[i + 1])
        }

        header_spec_list.append(header_spec)

    # parse lines
    if cleandata:
        for entry in cleandata:
            output_line = {}

            # insert new separator since data can contain spaces
            for col in reversed(header_list):
                # find the right header_spec
                for h_spec in header_spec_list:
                    if h_spec['name'] == col:
                        h_end = h_spec['end']
                        # check if the location contains whitespace. if not
                        # then move to the left until a space is found
                        while h_end > 0 and entry[h_end] not in string.whitespace:
                            h_end -= 1

                        # insert custom delimiter
                        entry = entry[:h_end] + delim + entry[h_end + 1:]

            # create the entry list from the new custom delimiter
            entry_list = entry.split(delim, maxsplit=len(header_list) - 1)

            # clean up leading and trailing spaces in entry
            clean_entry_list = []
            for col in entry_list:
                clean_entry = col.strip().rstrip()
                if clean_entry == '':
                    clean_entry = None
                
                clean_entry_list.append(clean_entry)

            output_line = dict(zip(header_list, clean_entry_list))
            raw_output.append(output_line)

        # clean up non-ascii characters, if any
        for entry in raw_output:
            entry['name'] = entry['name'].encode('ascii', errors='ignore').decode()

    if raw:
        return raw_output
    else:
        return process(raw_output)
