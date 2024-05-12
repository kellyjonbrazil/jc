[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.pci_ids"></a>

# jc.parsers.pci_ids

jc - JSON Convert `pci.ids` file parser

This parser converts the pci.ids database file.

https://raw.githubusercontent.com/pciutils/pciids/master/pci.ids

A nested schema allows straightforward queries with tools like `jq`. Hex id
numbers are prefixed with an underscore (`_`) so bracket notation is not
necessary when referencing. For example:

    $ cat pci.ids | jc --pci-ids | jq '.vendors._9005._0053._9005._ffff.subsystem_name'
    "AIC-7896 SCSI Controller mainboard implementation"

Here are the vendor and class mappings:

    jq '.vendors._001c._0001._001c._0005.subsystem_name'
                  |     |     |     |
                  |     |     |     subdevice
                  |     |     subvendor
                  |     device
                  vendor

    jq '.classes._0c._03._40'
                  |   |   |
                  |   |   prog_if
                  |   subclass
                  class

Usage (cli):

    $ cat pci.ids | jc --pci-ids

Usage (module):

    import jc
    result = jc.parse('pci_ids', pci_ids_file_output)

Schema:

    {
      "vendors": {
        "_<vendor_id>": {
          "vendor_name":                 string,
          "_<device_id>": {
            "device_name":               string,
            "_<subvendor_id>": {
              "_<subdevice_id":          string
            }
          }
        }
      },
      "classes": {
        "_<class_id>": {
          "class_name":                  string,
          "_<subclass_id>": {
            "subclass_name":             string,
            "_<prog_if>":                string
          }
        }
      }
    }

Examples:

    $ cat pci.ids | jc --pci-ids | jq '.vendors._001c._0001._001c._0005.subsystem_name'
    "2 Channel CAN Bus SJC1000 (Optically Isolated)"

    $ cat pci.ids | jc --pci-ids | jq '.classes._0c._03._40'
    "USB4 Host Interface"

<a id="jc.parsers.pci_ids.parse"></a>

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
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/pci_ids.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/pci_ids.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
