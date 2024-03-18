[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.lsattr"></a>

# jc.parsers.lsattr

jc - JSON Convert `lsattr` command output parser

Usage (cli):

    $ lsattr | jc --lsattr

or

    $ jc lsattr

Usage (module):

    import jc
    result = jc.parse('lsattr', lsattr_command_output)

Schema:

Information from https://github.com/mirror/busybox/blob/2d4a3d9e6c1493a9520b907e07a41aca90cdfd94/e2fsprogs/e2fs_lib.c#L40
used to define field names

    [
      {
        "file":                           string,
        "compressed_file":                Optional[boolean],
        "compressed_dirty_file":          Optional[boolean],
        "compression_raw_access":         Optional[boolean],
        "secure_deletion":                Optional[boolean],
        "undelete":                       Optional[boolean],
        "synchronous_updates":            Optional[boolean],
        "synchronous_directory_updates":  Optional[boolean],
        "immutable":                      Optional[boolean],
        "append_only":                    Optional[boolean],
        "no_dump":                        Optional[boolean],
        "no_atime":                       Optional[boolean],
        "compression_requested":          Optional[boolean],
        "encrypted":                      Optional[boolean],
        "journaled_data":                 Optional[boolean],
        "indexed_directory":              Optional[boolean],
        "no_tailmerging":                 Optional[boolean],
        "top_of_directory_hierarchies":   Optional[boolean],
        "extents":                        Optional[boolean],
        "no_cow":                         Optional[boolean],
        "casefold":                       Optional[boolean],
        "inline_data":                    Optional[boolean],
        "project_hierarchy":              Optional[boolean],
        "verity":                         Optional[boolean],
      }
    ]

Examples:

      $ sudo lsattr /etc/passwd | jc --lsattr
      [
        {
            "file": "/etc/passwd",
            "extents": true
        }
      ]

<a id="jc.parsers.lsattr.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/lsattr.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/lsattr.py)

Version 1.0 by Mark Rotner (rotner.mr@gmail.com)
