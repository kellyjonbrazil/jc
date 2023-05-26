"""jc - JSON Convert `lsattr` command output parser

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
        "Compressed_File":                Optional[boolean],
        "Compressed_Dirty_File":          Optional[boolean],
        "Compression_Raw_Access":         Optional[boolean],
        "Secure_Deletion":                Optional[boolean],
        "Undelete":                       Optional[boolean],
        "Synchronous_Updates":            Optional[boolean],
        "Synchronous_Directory_Updates":  Optional[boolean],
        "Immutable":                      Optional[boolean],
        "Append_Only":                    Optional[boolean],
        "No_Dump":                        Optional[boolean],
        "No_Atime":                       Optional[boolean],
        "Compression_Requested":          Optional[boolean],
        "Encrypted":                      Optional[boolean],
        "Journaled_Data":                 Optional[boolean],
        "Indexed_directory":              Optional[boolean],
        "No_Tailmerging":                 Optional[boolean],
        "Top_of_Directory_Hierarchies":   Optional[boolean],
        "Extents":                        Optional[boolean],
        "No_COW":                         Optional[boolean],
        "Casefold":                       Optional[boolean],
        "Inline_Data":                    Optional[boolean],
        "Project_Hierarchy":              Optional[boolean],
        "Verity":                         Optional[boolean],
      }
    ]

Examples:

      $ sudo lsattr /etc/passwd | jc --lsattr
      [
        {
            "file": "/etc/passwd",
            "Extents": true
        }
      ]
"""

import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`lsattr` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['lsattr']
    tags = ['command']


__version__ = info.version


ERROR_PREFIX = "lsattr:"

# https://github.com/mirror/busybox/blob/2d4a3d9e6c1493a9520b907e07a41aca90cdfd94/e2fsprogs/e2fs_lib.c#L40
# https://github.com/landley/toybox/blob/f1682dc79fd75f64042b5438918fe5a507977e1c/toys/other/lsattr.c#L97
ATTRIBUTES = {
    "B": "Compressed_File",
    "Z": "Compressed_Dirty_File",
    "X": "Compression_Raw_Access",
    "s": "Secure_Deletion",
    "u": "Undelete",
    "S": "Synchronous_Updates",
    "D": "Synchronous_Directory_Updates",
    "i": "Immutable",
    "a": "Append_Only",
    "d": "No_Dump",
    "A": "No_Atime",
    "c": "Compression_Requested",
    "E": "Encrypted",
    "j": "Journaled_Data",
    "I": "Indexed_directory",
    "t": "No_Tailmerging",
    "T": "Top_of_Directory_Hierarchies",
    "e": "Extents",
    "C": "No_COW",
    "F": "Casefold",
    "N": "Inline_Data",
    "P": "Project_Hierarchy",
    "V": "Verity",
}


def parse(data: str, quiet: bool = False):
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

    output = []

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

        line_output = {}

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
