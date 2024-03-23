r"""jc - JSON Convert `apt-cache show` command parser

Usage (cli):

    $ apt-cache show | jc --apt-cache-show

Usage (module):

    import jc
    result = jc.parse('apt_cache_show', apt_cache_show_output)

Schema:

    [
      {
        "package":                string,
        "version":                string,
        "installed_size":         integer,
        "maintainer":             string,
        "architecture":           string,
        "depends": [
                                  string
        ],
        "pre_depends": [
                                  string
        ],
        "recommends": [
                                  string
        ],
        "suggests": [
                                  string
        ],
        "conflicts": [
                                  string
        ],
        "breaks": [
                                  string
        ],
        "description_md5":        string,
        "multi_arch":             string,
        "homepage":               string,
        "section":                string,
        "priority":               string,
        "filename":               string,
        "size":                   integer,
        "sha256":                 string,
        "description":            string
      }
    ]

Examples:

    $ apt-cache show | jc --apt-cache-show -p
    [
      {
        "package": "systemd",
        "version": "247.3-6~bpo10+1",
        "installed_size": 16121,
        "maintainer": "Debian systemd Maintainers <pkg-systemd-maintaine..",
        "architecture": "amd64",
        "depends": [
          "libacl1 (>= 2.2.23)",
          "libapparmor1 (>= 2.13)",
          "libaudit1 (>= 1:2.2.1)",
          "libcap2 (>= 1:2.10)",
          "libcryptsetup12 (>= 2:2.0.1)",
          "libgnutls30 (>= 3.6.6)",
          "libgpg-error0 (>= 1.14)",
          "libip4tc0 (>= 1.6.0+snapshot20161117)",
          "libkmod2 (>= 5~)",
          "liblz4-1 (>= 0.0~r130)",
          "libmount1 (>= 2.30)",
          "libpam0g (>= 0.99.7.1)",
          "libseccomp2 (>= 2.3.1)",
          "libsystemd0 (= 247.3-6~bpo10+1)",
          "systemd-timesyncd | time-daemon",
          "util-linux (>= 2.27.1)",
          "mount (>= 2.26)",
          "adduser"
        ],
        "pre_depends": [
          "libblkid1 (>= 2.24)",
          "libc6 (>= 2.28)",
          "libgcrypt20 (>= 1.8.0)",
          "liblz4-1 (>= 0.0~r122)",
          "liblzma5 (>= 5.1.1alpha+20120614)",
          "libselinux1 (>= 2.1.9)",
          "libzstd1 (>= 1.4.0)"
        ],
        "recommends": [
          "dbus"
        ],
        "suggests": [
          "systemd-container",
          "policykit-1"
        ],
        "conflicts": [
          "consolekit",
          "libpam-ck-connector"
        ],
        "breaks": [
          "python-dbusmock (<< 0.18)",
          "python3-dbusmock (<< 0.18)",
          "resolvconf (<< 1.83~)",
          "systemd-shim (<< 10-4~)",
          "udev (<< 247~)"
        ],
        "description_md5": "19399579cbc0c47a303288bf15eadcd4",
        "multi_arch": "foreign",
        "homepage": "https://www.freedesktop.org/wiki/Software/systemd",
        "section": "admin",
        "priority": "important",
        "filename": "pool/main/s/systemd/systemd_247.3-6~bpo10+1_amd64.deb",
        "size": 4382056,
        "sha256": "2035450655ad02faa0f75dc952128b503e51df5795c67273c0f6...",
        "description": "system and service manager  systemd is a system..."
      },
      ...
    ]

    $ apt-cache show | jc --apt-cache-show -p -r
    [
      {
        "package": "systemd",
        "version": "247.3-6~bpo10+1",
        "installed_size": "16121",
        "maintainer": "Debian systemd Maintainers <pkg-systemd-maintain...",
        "architecture": "amd64",
        "depends": "libacl1 (>= 2.2.23), libapparmor1 (>= 2.13), libaud...",
        "pre_depends": "libblkid1 (>= 2.24), libc6 (>= 2.28), libgcrypt...",
        "recommends": "dbus",
        "suggests": "systemd-container, policykit-1",
        "conflicts": "consolekit, libpam-ck-connector",
        "breaks": "python-dbusmock (<< 0.18), python3-dbusmock (<< 0.18...",
        "description_md5": "19399579cbc0c47a303288bf15eadcd4",
        "multi_arch": "foreign",
        "homepage": "https://www.freedesktop.org/wiki/Software/systemd",
        "section": "admin",
        "priority": "important",
        "filename": "pool/main/s/systemd/systemd_247.3-6~bpo10+1_amd64.deb",
        "size": "4382056",
        "sha256": "2035450655ad02faa0f75dc952128b503e51df5795c67273c0f6...",
        "description": "system and service manager  systemd is a system..."
      },
      ...
    ]
"""
from typing import List
from jc.jc_types import JSONDictType
import jc.parsers.rpm_qi as rpm_qi


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`apt-cache show` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the rpm-qi parser'
    compatible = ['linux']
    tags = ['command']
    magic_commands = ['apt-cache show']


__version__ = info.version


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
    # This parser is an alias of rpm_qi.py
    rpm_qi.info = info  # type: ignore
    rpm_qi.__name__ = __name__
    return rpm_qi.parse(data, raw, quiet)
