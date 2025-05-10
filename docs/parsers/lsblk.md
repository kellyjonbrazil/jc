[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.lsblk"></a>

# jc.parsers.lsblk

jc - JSON Convert `lsblk` command output parser

Usage (cli):

    $ lsblk | jc --lsblk

or

    $ jc lsblk

Usage (module):

    import jc
    result = jc.parse('lsblk', lsblk_command_output)

Schema:

    [
      {
        "name":             string,
        "maj_min":          string,
        "rm":               boolean,
        "size":             string,
        "size_bytes":       integer
        "ro":               boolean,
        "type":             string,
        "mountpoint":       string,
        "mountpoints": [
                            string
        ],
        "kname":            string,
        "fstype":           string,
        "label":            string,
        "uuid":             string,
        "partlabel":        string,
        "partuuid":         string,
        "ra":               integer,
        "model":            string,
        "serial":           string,
        "state":            string,
        "owner":            string,
        "group":            string,
        "mode":             string,
        "alignment":        integer,
        "min_io":           integer,
        "opt_io":           integer,
        "phy_sec":          integer,
        "log_sec":          integer,
        "rota":             boolean,
        "sched":            string,
        "rq_size":          integer,
        "disc_aln":         integer,
        "disc_gran":        string,
        "disc_gran_bytes":  integer,
        "disc_max":         string,
        "disc_max_bytes":   integer,
        "disc_zero":        boolean,
        "wsame":            string,
        "wsame_bytes":      integer,
        "wwn":              string,
        "rand":             boolean,
        "pkname":           string,
        "hctl":             string,
        "tran":             string,
        "rev":              string,
        "vendor":           string
      }
    ]

Examples:

    $ lsblk | jc --lsblk -p
    [
      {
        "name": "sda",
        "maj_min": "8:0",
        "rm": false,
        "size": "20G",
        "size_bytes": 20000000000,
        "ro": false,
        "type": "disk",
        "mountpoint": null
      },
      {
        "name": "sda1",
        "maj_min": "8:1",
        "rm": false,
        "size": "1G",
        "size_bytes": 1000000000
        "ro": false,
        "type": "part",
        "mountpoint": "/boot"
      },
      ...
    ]

    $ lsblk -o +KNAME,FSTYPE,LABEL,UUID,PARTLABEL,PARTUUID,RA,MODEL,SERIAL,\\
      STATE,OWNER,GROUP,MODE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,\\
      SCHED,RQ-SIZE,DISC-ALN,DISC-GRAN,DISC-MAX,DISC-ZERO,WSAME,WWN,RAND,\\
      PKNAME,HCTL,TRAN,REV,VENDOR | jc --lsblk -p
    [
      {
        "name": "sda",
        "maj_min": "8:0",
        "rm": false,
        "size": "20G",
        "size_bytes": 20000000000,
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
        "disc_gran_bytes": 0,
        "disc_max": "0B",
        "disc_max_bytes": 0,
        "disc_zero": false,
        "wsame": "32M",
        "wsame_bytes": 32000000,
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
        "size_bytes": 1000000000
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
        "disc_gran_bytes": 0,
        "disc_max": "0B",
        "disc_max_bytes": 0,
        "disc_zero": false,
        "wsame": "32M",
        "wsame_bytes": 32000000,
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

    $ lsblk -o +KNAME,FSTYPE,LABEL,UUID,PARTLABEL,PARTUUID,RA,MODEL,SERIAL,\\
      STATE,OWNER,GROUP,MODE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,\\
      SCHED,RQ-SIZE,DISC-ALN,DISC-GRAN,DISC-MAX,DISC-ZERO,WSAME,WWN,RAND,\\
      PKNAME,HCTL,TRAN,REV,VENDOR | jc --lsblk -p -r
    [
      {
        "name": "sda",
        "maj_min": "8:0",
        "rm": "0",
        "size": "20G",
        "size_bytes": 20000000000,
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
        "disc_gran_bytes": 0,
        "disc_max": "0B",
        "disc_max_bytes": 0,
        "disc_zero": "0",
        "wsame": "32M",
        "wsame_bytes": 32000000,
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
        "size_bytes": 1000000000
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
        "disc_gran_bytes": 0,
        "disc_max": "0B",
        "disc_max_bytes": 0,
        "disc_zero": "0",
        "wsame": "32M",
        "wsame_bytes": 32000000,
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

<a id="jc.parsers.lsblk.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/lsblk.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/lsblk.py)

Version 1.10 by Kelly Brazil (kellyjonbrazil@gmail.com)
