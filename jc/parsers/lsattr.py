r"""jc - JSON Convert `lsattr` command output parser

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
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`lsattr` command parser'
    author = 'Mark Rotner'
    author_email = 'rotner.mr@gmail.com'
    compatible = ['linux']
    magic_commands = ['lsattr']
    tags = ['command']


__version__ = info.version


ERROR_PREFIX = "lsattr:"

# https://github.com/mirror/busybox/blob/2d4a3d9e6c1493a9520b907e07a41aca90cdfd94/e2fsprogs/e2fs_lib.c#L40
# https://github.com/landley/toybox/blob/f1682dc79fd75f64042b5438918fe5a507977e1c/toys/other/lsattr.c#L97
ATTRIBUTES = {
    "B": "compressed_file",
    "Z": "compressed_dirty_file",
    "X": "compression_raw_access",
    "s": "secure_deletion",
    "u": "undelete",
    "S": "synchronous_updates",
    "D": "synchronous_directory_updates",
    "i": "immutable",
    "a": "append_only",
    "d": "no_dump",
    "A": "no_atime",
    "c": "compression_requested",
    "E": "encrypted",
    "j": "journaled_data",
    "I": "indexed_directory",
    "t": "no_tailmerging",
    "T": "top_of_directory_hierarchies",
    "e": "extents",
    "C": "no_cow",
    "F": "casefold",
    "N": "inline_data",
    "P": "project_hierarchy",
    "V": "verity",
}


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    output: List = []

    cleandata = list(filter(None, data.splitlines()))

    if not jc.utils.has_data(data):
        return output

    for line in cleandata:
        # -R flag returns the output in the format:
        # Folder:
        #   attributes file_in_folder
        if line.endswith(':'):
            continue

        # lsattr: Operation not supported ....
        if line.startswith(ERROR_PREFIX):
            continue

        line_output: Dict = {}

        # attributes file
        # --------------e----- /etc/passwd
        attributes, file = line.split()
        line_output['file'] = file
        for attribute in list(attributes):
            attribute_key = ATTRIBUTES.get(attribute)
            if attribute_key:
                line_output[attribute_key] = True

        if line_output:
            output.append(line_output)

    return output
