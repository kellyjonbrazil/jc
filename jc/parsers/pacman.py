r"""jc - JSON Convert `pacman` command output parser

Supports the following `pacman` arguments:

- `-Si`
- `-Sii`
- `-Qi`
- `-Qii`

The `*_epoch` calculated timestamp fields are naive. (i.e. based on the
local time of the system the parser is run on)

Usage (cli):

    $ pacman -Si <package> | jc --pacman

or

    $ jc pacman -Si <package>

Usage (module):

    import jc
    result = jc.parse('pacman', pacman_command_output)

Schema:

    [
      {
        "repository":               string,
        "name":                     string,
        "version":                  string,
        "description":              string,
        "architecture":             string,
        "url":                      string,
        "licenses": [
                                    string
        ],
        "groups": [
                                    string
        ],
        "provides": [
                                    string
        ],
        "depends_on": [
                                    string
        ],
        "optional_deps": [
          {
            "name":                 string,
            "description":          string
          }
        ],
        "optional_for": [
                                    string
        ],
        "conflicts_with": [
                                    string
        ],
        "replaces": [
                                    string
        ],
        "download_size":            string,
        "download_size_bytes":      integer     [0]
        "installed_size":           string,
        "installed_size_bytes":     integer,    [0]
        "packager":                 string,
        "build_date":               string,
        "build_date_epoch":         integer,    [0]
        "install_date":             string,
        "install_date_epoch":       integer,    [0]
        "validated_by": [
                                    string
        ],
        "backup_files": [
                                    string
        ]
      }
    ]

    [0] Field exists if conversion successful

Examples:

    $ pacman -qii zstd | jc --pacman -p
    [
      {
        "name": "zstd",
        "version": "1.5.6-1",
        "description": "Zstandard - Fast real-time compression algorithm",
        "architecture": "x86_64",
        "url": "https://facebook.github.io/zstd/",
        "licenses": [
          "BSD-3-Clause",
          "GPL-2.0-only"
        ],
        "groups": [],
        "provides": [
          "libzstd.so=1-64"
        ],
        "depends_on": [
          "glibc",
          "gcc-libs",
          "zlib",
          "xz",
          "lz4"
        ],
        "required_by": [
          "android-tools",
          "appstream",
          ...
          "tiled",
          "vulkan-radeon",
          "wireshark-cli"
        ],
        "optional_for": [
          "xarchiver"
        ],
        "conflicts_with": [],
        "replaces": [],
        "installed_size": "1527.00 KiB",
        "installed_size_bytes": 1563648,
        "packager": "Levente Polyak <anthraxx@archlinux.org>",
        "build_date": "Sat 11 May 2024 06:14:19 AM +08",
        "build_date_epoch": 1715433259,
        "install_date": "Fri 24 May 2024 09:50:31 AM +08",
        "install_date_epoch": 1715663342,
        "install_reason": "Installed as a dependency for another package",
        "install_script": "No",
        "validated_by": [
          "Signature"
        ],
        "extended_data": "pkgtype=pkg"
      }
    ]

    $ pacman -qii zstd | jc --pacman -p -r
    [
      {
        "name": "zstd",
        "version": "1.5.6-1",
        "description": "Zstandard - Fast real-time compression algorithm",
        "architecture": "x86_64",
        "url": "https://facebook.github.io/zstd/",
        "licenses": "BSD-3-Clause  GPL-2.0-only",
        "groups": null,
        "provides": "libzstd.so=1-64",
        "depends_on": "glibc  gcc-libs  zlib  xz  lz4",
        "required_by": [
          "android-tools  appstream  avr-gcc  binutils  blender  blosc",
          "boost-libs  btrfs-progs  cloudflare-warp-bin  comgr  curl",
          "dolphin-emu  file  flatpak  gcc  gdal  gnutls  karchive",
          "karchive5  kmod  lib32-zstd  libarchive  libelf  libtiff",
          "libva-mesa-driver  libxmlb  libzip  lld  llvm-libs  mariadb-libs",
          "mesa  mesa-vdpau  minizip-ng  mkinitcpio  mold  netcdf",
          "opencl-clover-mesa  opencl-rusticl-mesa  openucx  postgresql",
          "postgresql-libs  ppsspp  qemu-img  qemu-system-riscv",
          "qemu-system-x86  qgis  qt6-base  qt6-tools  rsync  rustup",
          "squashfs-tools  squashfuse  systemd-libs  tiled  vulkan-radeon",
          "wireshark-cli"
        ],
        "optional_for": "xarchiver",
        "conflicts_with": null,
        "replaces": null,
        "installed_size": "1527.00 KiB",
        "packager": "Levente Polyak <anthraxx@archlinux.org>",
        "build_date": "Sat 11 May 2024 06:14:19 AM +08",
        "install_date": "Fri 24 May 2024 09:50:31 AM +08",
        "install_reason": "Installed as a dependency for another package",
        "install_script": "No",
        "validated_by": "Signature",
        "extended_data": "pkgtype=pkg"
      }
    ]
"""
from typing import List, Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`pacman` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['command', 'file']
    magic_commands = ['pacman']


__version__ = info.version


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    split_fields = {
        'licenses', 'groups', 'provides', 'depends_on', 'conflicts_with',
        'replaces', 'optional_for'
    }
    space_split_fields = {
        'required_by', 'groups', 'provides', 'depends_on',
        'conflicts_with', 'replaces', 'validated_by'
    }
    two_space_fields = {'licenses', 'validated_by'}
    name_description_fields = {'optional_deps'}
    size_fields = {'download_size', 'installed_size'}
    date_fields = {'build_date', 'install_date'}

    # initial split for field lists
    for item in proc_data:
        for key, val in item.copy().items():
            if key in split_fields:
                if val is None:
                    item[key] = []
                else:
                    item[key] = val.split()

            # fixup for specific lists
            if key in space_split_fields and isinstance(val, List):
                val_list = [x.split() for x in val]
                item[key] = [x for xs in val_list for x in xs]  # flatten the list

            if key in two_space_fields and isinstance(val, str):
                item[key] = val.split('  ')

            if key in name_description_fields and isinstance(val, list):
                new_list = []
                for name_desc in val:
                    n, *d = name_desc.split(': ')
                    if d == []:
                        d = ''
                    else:
                        d = d[0]
                    new_obj = {'name': n, 'description': d}
                    new_list.append(new_obj)
                item[key] = new_list

            if key in size_fields:
                bts = jc.utils.convert_size_to_int(val)
                if bts:
                    item[key + '_bytes'] = bts

            if key in date_fields:
                # need to append '00' to date for conversion
                ts = jc.utils.timestamp(val + '00', format_hint=(3100,))
                if ts.naive:
                    item[key + '_epoch'] = ts.naive
                else:
                    # try taking off the text TZ identifier
                    ts = jc.utils.timestamp(val[:-4], format_hint=(3000,))
                    if ts.naive:
                        item[key + '_epoch'] = ts.naive

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[Dict] = []
    entry_obj: Dict = {}
    multiline_fields = {'required_by', 'optional_deps', 'backup_files'}
    multiline_list: List = []
    multiline_key = ''

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            splitline = line.split(' : ', maxsplit=1)

            if len(splitline) == 2:
                # this is a key/value pair
                key, val = splitline
                key = key.strip()
                key = jc.utils.normalize_key(key)
                val = val.strip()

                # new entries can start with "Repository" or "Name"
                if (key == 'name' or key == 'repository') and len(entry_obj) > 2:
                    if multiline_list:
                        entry_obj[multiline_key] = multiline_list
                        multiline_list = []
                        multiline_key = ''
                    if entry_obj:
                        raw_output.append(entry_obj)
                    entry_obj = {}
                    entry_obj[key] = val
                    continue

                if key in multiline_fields:
                    if multiline_list:
                        entry_obj[multiline_key] = multiline_list
                    multiline_list = []
                    if val != 'None':
                        multiline_list.append(val)
                    multiline_key = key
                    continue

                if key not in multiline_fields:
                    if multiline_list:
                        entry_obj[multiline_key] = multiline_list
                        multiline_list = []
                        multiline_key = ''
                    entry_obj[key] = val if val != 'None' else None
                    continue

            # multiline field continuation lines
            multiline_list.append(line.strip())
            continue

        # grab the last entry
        if entry_obj:
            if multiline_list:
                entry_obj[multiline_key] = multiline_list
                multiline_list = []
                multiline_key = ''
            raw_output.append(entry_obj)

    return raw_output if raw else _process(raw_output)
