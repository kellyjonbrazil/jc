[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.getfacl"></a>

# jc.parsers.getfacl

jc - JSON Convert `getfacl` command output parser

Parses the default (non-tabular) `getfacl` output. The file name, owner, and
owning group from the comment header are included on every entry, along with
the setuid/setgid/sticky `# flags` value when `getfacl` prints that line.

Each ACL entry is returned as a separate item. The `effective` field is
populated from the `#effective` comment, which is only printed when the
effective rights differ from the entry's own rights unless `getfacl -e` is
used. `default` is `true` for entries in a directory's default ACL.

The `-t`/`--tabular` output format is not supported.

Usage (cli):

    $ getfacl file.txt | jc --getfacl

or

    $ jc getfacl file.txt

Usage (module):

    import jc
    result = jc.parse('getfacl', getfacl_command_output)

Schema:

    [
      {
        "file":             string/null,
        "owner":            string/null,
        "group":            string/null,
        "flags":            string/null,
        "type":             string,
        "name":             string/null,
        "permissions":      string,
        "effective":        string/null,
        "default":          boolean
      }
    ]

Examples:

    $ getfacl file.txt | jc --getfacl -p
    [
      {
        "file": "file.txt",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": null,
        "type": "user",
        "name": null,
        "permissions": "rw-",
        "effective": null,
        "default": false
      },
      {
        "file": "file.txt",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": null,
        "type": "user",
        "name": "root",
        "permissions": "rwx",
        "effective": "r--",
        "default": false
      },
      {
        "file": "file.txt",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": null,
        "type": "group",
        "name": null,
        "permissions": "rw-",
        "effective": "r--",
        "default": false
      },
      {
        "file": "file.txt",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": null,
        "type": "mask",
        "name": null,
        "permissions": "r--",
        "effective": null,
        "default": false
      },
      {
        "file": "file.txt",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": null,
        "type": "other",
        "name": null,
        "permissions": "r--",
        "effective": null,
        "default": false
      }
    ]

    $ getfacl dir | jc --getfacl -p
    [
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "user",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": false
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "user",
        "name": "root",
        "permissions": "r-x",
        "effective": null,
        "default": false
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "group",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": false
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "mask",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": false
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "other",
        "name": null,
        "permissions": "r-x",
        "effective": null,
        "default": false
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "user",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": true
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "user",
        "name": "root",
        "permissions": "rwx",
        "effective": null,
        "default": true
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "group",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": true
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "mask",
        "name": null,
        "permissions": "rwx",
        "effective": null,
        "default": true
      },
      {
        "file": "dir",
        "owner": "tunglpb",
        "group": "tunglpb",
        "flags": "-s-",
        "type": "other",
        "name": null,
        "permissions": "r-x",
        "effective": null,
        "default": true
      }
    ]

<a id="jc.parsers.getfacl.parse"></a>

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

Source: [`jc/parsers/getfacl.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/getfacl.py)

Version 1.0 by Tung Lam (53996158+tunglambk@users.noreply.github.com)
