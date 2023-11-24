"""jc - JSON Convert `tune2fs -l` command output parser

Usage (cli):

    $ tune2fs -l /dev/xvda4 | jc --tune2fs

or

    $ jc tune2fs -l /dev/xvda4

Usage (module):

    import jc
    result = jc.parse('tune2fs', tune2fs_command_output)

Schema:

    {
      "version":                            string,
      "filesystem_volume_name":             string,
      "last_mounted_on":                    string,
      "filesystem_uuid":                    string,
      "filesystem_magic_number":            string,
      "filesystem_revision_number":         string,
      "filesystem_features": [
                                            string
      ],
      "filesystem_flags":                   string,
      "default_mount_options":              string,
      "filesystem_state":                   string,
      "errors_behavior":                    string,
      "filesystem_os_type":                 string,
      "inode_count":                        integer,
      "block_count":                        integer,
      "reserved_block_count":               integer,
      "overhead_clusters":                  integer,
      "free_blocks":                        integer,
      "free_inodes":                        integer,
      "first_block":                        integer,
      "block_size":                         integer,
      "fragment_size":                      integer,
      "group_descriptor_size":              integer,
      "reserved_gdt_blocks":                integer,
      "blocks_per_group":                   integer,
      "fragments_per_group":                integer,
      "inodes_per_group":                   integer,
      "inode_blocks_per_group":             integer,
      "flex_block_group_size":              integer,
      "filesystem_created":                 string,
      "filesystem_created_epoch":           integer,
      "filesystem_created_epoch_utc":       integer,
      "last_mount_time":                    string,
      "last_mount_time_epoch":              integer,
      "last_mount_time_epoch_utc":          integer,
      "last_write_time":                    string,
      "last_write_time_epoch":              integer,
      "last_write_time_epoch_utc":          integer,
      "mount_count":                        integer,
      "maximum_mount_count":                integer,
      "last_checked":                       string,
      "last_checked_epoch":                 integer,
      "last_checked_epoch_utc":             integer,
      "check_interval":                     string,
      "lifetime_writes":                    string,
      "reserved_blocks_uid":                string,
      "reserved_blocks_gid":                string,
      "first_inode":                        integer,
      "inode_size":                         integer,
      "required_extra_isize":               integer,
      "desired_extra_isize":                integer,
      "journal_inode":                      integer,
      "default_directory_hash":             string,
      "directory_hash_seed":                string,
      "journal_backup":                     string,
      "checksum_type":                      string,
      "checksum":                           string
    }

Examples:

    $ tune2fs | jc --tune2fs -p
    {
      "version": "1.46.2 (28-Feb-2021)",
      "filesystem_volume_name": "<none>",
      "last_mounted_on": "/home",
      "filesystem_uuid": "5fb78e1a-b214-44e2-a309-8e35116d8dd6",
      "filesystem_magic_number": "0xEF53",
      "filesystem_revision_number": "1 (dynamic)",
      "filesystem_features": [
        "has_journal",
        "ext_attr",
        "resize_inode",
        "dir_index",
        "filetype",
        "needs_recovery",
        "extent",
        "64bit",
        "flex_bg",
        "sparse_super",
        "large_file",
        "huge_file",
        "dir_nlink",
        "extra_isize",
        "metadata_csum"
      ],
      "filesystem_flags": "signed_directory_hash",
      "default_mount_options": "user_xattr acl",
      "filesystem_state": "clean",
      "errors_behavior": "Continue",
      "filesystem_os_type": "Linux",
      "inode_count": 3932160,
      "block_count": 15728640,
      "reserved_block_count": 786432,
      "free_blocks": 15198453,
      "free_inodes": 3864620,
      "first_block": 0,
      "block_size": 4096,
      "fragment_size": 4096,
      "group_descriptor_size": 64,
      "reserved_gdt_blocks": 1024,
      "blocks_per_group": 32768,
      "fragments_per_group": 32768,
      "inodes_per_group": 8192,
      "inode_blocks_per_group": 512,
      "flex_block_group_size": 16,
      "filesystem_created": "Mon Apr  6 15:10:37 2020",
      "last_mount_time": "Mon Sep 19 15:16:20 2022",
      "last_write_time": "Mon Sep 19 15:16:20 2022",
      "mount_count": 14,
      "maximum_mount_count": -1,
      "last_checked": "Fri Apr  8 15:24:22 2022",
      "check_interval": "0 (<none>)",
      "lifetime_writes": "203 GB",
      "reserved_blocks_uid": "0 (user root)",
      "reserved_blocks_gid": "0 (group root)",
      "first_inode": 11,
      "inode_size": 256,
      "required_extra_isize": 32,
      "desired_extra_isize": 32,
      "journal_inode": 8,
      "default_directory_hash": "half_md4",
      "directory_hash_seed": "67d5358d-723d-4ce3-b3c0-30ddb433ad9e",
      "journal_backup": "inode blocks",
      "checksum_type": "crc32c",
      "checksum": "0x7809afff",
      "filesystem_created_epoch": 1586211037,
      "filesystem_created_epoch_utc": null,
      "last_mount_time_epoch": 1663625780,
      "last_mount_time_epoch_utc": null,
      "last_write_time_epoch": 1663625780,
      "last_write_time_epoch_utc": null,
      "last_checked_epoch": 1649456662,
      "last_checked_epoch_utc": null
    }

    $ tune2fs | jc --tune2fs -p -r
    {
      "version": "1.46.2 (28-Feb-2021)",
      "filesystem_volume_name": "<none>",
      "last_mounted_on": "/home",
      "filesystem_uuid": "5fb78e1a-b214-44e2-a309-8e35116d8dd6",
      "filesystem_magic_number": "0xEF53",
      "filesystem_revision_number": "1 (dynamic)",
      "filesystem_features": "has_journal ext_attr resize_inode dir_index filetype needs_recovery extent 64bit flex_bg sparse_super large_file huge_file dir_nlink extra_isize metadata_csum",
      "filesystem_flags": "signed_directory_hash",
      "default_mount_options": "user_xattr acl",
      "filesystem_state": "clean",
      "errors_behavior": "Continue",
      "filesystem_os_type": "Linux",
      "inode_count": "3932160",
      "block_count": "15728640",
      "reserved_block_count": "786432",
      "free_blocks": "15198453",
      "free_inodes": "3864620",
      "first_block": "0",
      "block_size": "4096",
      "fragment_size": "4096",
      "group_descriptor_size": "64",
      "reserved_gdt_blocks": "1024",
      "blocks_per_group": "32768",
      "fragments_per_group": "32768",
      "inodes_per_group": "8192",
      "inode_blocks_per_group": "512",
      "flex_block_group_size": "16",
      "filesystem_created": "Mon Apr  6 15:10:37 2020",
      "last_mount_time": "Mon Sep 19 15:16:20 2022",
      "last_write_time": "Mon Sep 19 15:16:20 2022",
      "mount_count": "14",
      "maximum_mount_count": "-1",
      "last_checked": "Fri Apr  8 15:24:22 2022",
      "check_interval": "0 (<none>)",
      "lifetime_writes": "203 GB",
      "reserved_blocks_uid": "0 (user root)",
      "reserved_blocks_gid": "0 (group root)",
      "first_inode": "11",
      "inode_size": "256",
      "required_extra_isize": "32",
      "desired_extra_isize": "32",
      "journal_inode": "8",
      "default_directory_hash": "half_md4",
      "directory_hash_seed": "67d5358d-723d-4ce3-b3c0-30ddb433ad9e",
      "journal_backup": "inode blocks",
      "checksum_type": "crc32c",
      "checksum": "0x7809afff"
    }
"""
from typing import Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`tune2fs -l` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['tune2fs -l']


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    int_list = {'inode_count', 'block_count', 'reserved_block_count', 'free_blocks',
                'free_inodes', 'first_block', 'block_size', 'fragment_size',
                'group_descriptor_size', 'reserved_gdt_blocks', 'blocks_per_group',
                'fragments_per_group', 'inodes_per_group', 'inode_blocks_per_group',
                'flex_block_group_size', 'mount_count', 'maximum_mount_count',
                'first_inode', 'inode_size', 'required_extra_isize', 'desired_extra_isize',
                'journal_inode', 'overhead_clusters'}

    datetime_list = {'filesystem_created', 'last_mount_time', 'last_write_time', 'last_checked'}

    for key in proc_data:
        if key in int_list:
            proc_data[key] = jc.utils.convert_to_int(proc_data[key])

    for key in proc_data.copy():
        if key in datetime_list:
            dt = jc.utils.timestamp(proc_data[key], (1000,))
            proc_data[key + '_epoch'] = dt.naive
            proc_data[key + '_epoch_utc'] = dt.utc

    if 'filesystem_features' in proc_data:
        proc_data['filesystem_features'] = proc_data['filesystem_features'].split()

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> JSONDictType:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            if line.startswith('tune2fs '):
                raw_output['version'] = line.split(maxsplit=1)[1]
                continue

            linesplit = line.split(':', maxsplit=1)
            key = linesplit[0].lower().replace(' ', '_').replace('#', 'number')
            val = linesplit[1].strip()
            raw_output[key] = val

    return raw_output if raw else _process(raw_output)
