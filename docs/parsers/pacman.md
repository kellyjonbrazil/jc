[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.pacman"></a>

# jc.parsers.pacman

jc - JSON Convert `pacman` command output parser

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

<a id="jc.parsers.pacman.parse"></a>

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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/pacman.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/pacman.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
