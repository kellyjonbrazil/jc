[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.authorized_keys"></a>

# jc.parsers.authorized_keys

jc - JSON Convert `~/.ssh/authorized_keys` file parser

Comment lines (starting with `#`) and blank lines are ignored.

Usage (cli):

    $ cat ~/.ssh/authorized_keys | jc --authorized-keys

Usage (module):

    import jc
    result = jc.parse('authorized_keys', authorized_keys_file_output)

Schema:

    [
      {
        "type":            string,
        "key":             string,
        "options": [
                           string
        ],
        "comment":         string/null
      }
    ]

Examples:

    $ cat ~/.ssh/authorized_keys | jc --authorized-keys -p
    [
      {
        "options": [],
        "type": "ssh-ed25519",
        "key": "AAAAC3NzaC1lZDI1NTE5AAAAIHghxye3Vq/KsZ0sFBplo+n3lp/BWBJyDG2VzlIqynfX",
        "comment": "bob@laptop"
      },
      {
        "options": [
          "command=\"/usr/bin/rsync --server\"",
          "no-port-forwarding"
        ],
        "type": "ssh-rsa",
        "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDg0BAJ5uRurdBc7//UY1w4p7cuc8w...",
        "comment": null
      }
    ]

    $ cat ~/.ssh/authorized_keys | jc --authorized-keys -p -r
    [
      {
        "options": null,
        "type": "ssh-ed25519",
        "key": "AAAAC3NzaC1lZDI1NTE5AAAAIHghxye3Vq/KsZ0sFBplo+n3lp/BWBJyDG2VzlIqynfX",
        "comment": "bob@laptop"
      },
      {
        "options": "command=\"/usr/bin/rsync --server\",no-port-forwarding",
        "type": "ssh-rsa",
        "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDg0BAJ5uRurdBc7//UY1w4p7cuc8w...",
        "comment": null
      }
    ]

<a id="jc.parsers.authorized_keys.parse"></a>

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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/authorized_keys.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/authorized_keys.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
