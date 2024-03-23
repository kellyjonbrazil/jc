[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.veracrypt"></a>

# jc.parsers.veracrypt

jc - JSON Convert `veracrypt` command output parser

Supports the following `veracrypt` subcommands:
- `veracrypt --text --list`
- `veracrypt --text --list --verbose`
- `veracrypt --text --volume-properties <volume>`

Usage (cli):

    $ veracrypt --text --list | jc --veracrypt
or

    $ jc veracrypt --text --list

Usage (module):

    import jc
    result = jc.parse('veracrypt', veracrypt_command_output)

Schema:

    Volume:
    [
        {
            "slot":                 integer,
            "path":                 string,
            "device":               string,
            "mountpoint":           string,
            "size":                 string,
            "type":                 string,
            "readonly":             string,
            "hidden_protected":     string,
            "encryption_algo":      string,
            "pk_size":              string,
            "sk_size":              string,
            "block_size":           string,
            "mode":                 string,
            "prf":                  string,
            "format_version":       integer,
            "backup_header":        string
        }
    ]

Examples:

    $ veracrypt --text --list | jc --veracrypt -p
    [
        {
            "slot": 1,
            "path": "/dev/sdb1",
            "device": "/dev/mapper/veracrypt1",
            "mountpoint": "/home/bob/mount/encrypt/sdb1"
        }
    ]

    $ veracrypt --text --list --verbose | jc --veracrypt -p
    [
        {
            "slot": 1,
            "path": "/dev/sdb1",
            "device": "/dev/mapper/veracrypt1",
            "mountpoint": "/home/bob/mount/encrypt/sdb1",
            "size": "522 MiB",
            "type": "Normal",
            "readonly": "No",
            "hidden_protected": "No",
            "encryption_algo": "AES",
            "pk_size": "256 bits",
            "sk_size": "256 bits",
            "block_size": "128 bits",
            "mode": "XTS",
            "prf": "HMAC-SHA-512",
            "format_version": 2,
            "backup_header": "Yes"
        }
    ]

<a id="jc.parsers.veracrypt.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
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

Source: [`jc/parsers/veracrypt.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/veracrypt.py)

Version 1.0 by Jake Ob (iakopap at gmail.com)
