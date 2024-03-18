[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_cmdline"></a>

# jc.parsers.proc_cmdline

jc - JSON Convert `/proc/cmdline` file parser

Usage (cli):

    $ cat /proc/cmdline | jc --proc

or

    $ jc /proc/cmdline

or

    $ cat /proc/cmdline | jc --proc-cmdline

Usage (module):

    import jc
    result = jc.parse('proc_cmdline', proc_cmdline_file)

Schema:

    {
      "<key>":          string,
      "_options": [
                        string
      ]
    }

Examples:

    $ cat /proc/cmdline | jc --proc -p
    {
      "BOOT_IMAGE": "clonezilla/live/vmlinuz",
      "consoleblank": "0",
      "keyboard-options": "grp:ctrl_shift_toggle,lctrl_shift_toggle",
      "ethdevice-timeout": "130",
      "toram": "filesystem.squashfs",
      "boot": "live",
      "edd": "on",
      "ocs_daemonon": "ssh lighttpd",
      "ocs_live_run": "sudo screen /usr/sbin/ocs-sr -g auto -e1 auto -e2 -batch -r -j2 -k -scr -p true restoreparts win7-64 sda1",
      "ocs_live_extra_param": "",
      "keyboard-layouts": "us,ru",
      "ocs_live_batch": "no",
      "locales": "ru_RU.UTF-8",
      "vga": "788",
      "net.ifnames": "0",
      "union": "overlay",
      "fetch": "http://10.1.1.1/tftpboot/clonezilla/live/filesystem.squashfs",
      "ocs_postrun99": "sudo reboot",
      "initrd": "clonezilla/live/initrd.img",
      "_options": [
        "config",
        "noswap",
        "nolocales",
        "nomodeset",
        "noprompt",
        "nosplash",
        "nodmraid",
        "components"
      ]
    }

<a id="jc.parsers.proc_cmdline.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> Dict[str, Any]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc_cmdline.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_cmdline.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
