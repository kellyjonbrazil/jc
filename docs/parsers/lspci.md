[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.lspci"></a>

# jc.parsers.lspci

jc - JSON Convert `lspci -mmv` command output parser

This parser supports the following `lspci` options:
- `-mmv`
- `-nmmv`
- `-nnmmv`

Usage (cli):

    $ lspci -nnmmv | jc --lspci

or

    $ jc lspci -nnmmv

Usage (module):

    import jc
    result = jc.parse('lspci', lspci_command_output)

Schema:

    [
      {
        "slot":                         string,
        "domain":                       string,
        "domain_int":                   integer,
        "bus":                          string,
        "bus_int":                      integer,
        "dev":                          string,
        "dev_int":                      integer,
        "function":                     string,
        "function_int":                 integer,
        "class":                        string,
        "class_id":                     string,
        "class_id_int":                 integer,
        "vendor":                       string,
        "vendor_id":                    string,
        "vendor_id_int":                integer,
        "device":                       string,
        "device_id":                    string,
        "device_id_int":                integer,
        "svendor":                      string,
        "svendor_id":                   string,
        "svendor_id_int":               integer,
        "sdevice":                      string,
        "sdevice_id":                   string,
        "sdevice_id_int":               integer,
        "rev":                          string,
        "physlot":                      string,
        "progif":                       string,
        "progif_int":                   integer
      }
    ]

Examples:

    $ lspci -nnmmv | jc --lspci -p
    [
      {
        "slot": "ff:02:05.0",
        "domain": "ff",
        "domain_int": 255,
        "bus": "02",
        "bus_int": 2,
        "dev": "05",
        "dev_int": 5,
        "function": "0",
        "function_int": 0,
        "class": "SATA controller",
        "class_id": "0106",
        "class_id_int": 262,
        "vendor": "VMware",
        "vendor_id": "15ad",
        "vendor_id_int": 5549,
        "device": "SATA AHCI controller",
        "device_id": "07e0",
        "device_id_int": 2016,
        "svendor": "VMware",
        "svendor_id": "15ad",
        "svendor_id_int": 5549,
        "sdevice": "SATA AHCI controller",
        "sdevice_id": "07e0",
        "sdevice_id_int": 2016,
        "physlot": "37",
        "progif": "01",
        "progif_int": 1
      },
      ...
    ]

    $ lspci -nnmmv | jc --lspci -p -r
    [
      {
        "slot": "ff:02:05.0",
        "domain": "ff",
        "bus": "02",
        "dev": "05",
        "function": "0",
        "class": "SATA controller",
        "class_id": "0106",
        "vendor": "VMware",
        "vendor_id": "15ad",
        "device": "SATA AHCI controller",
        "device_id": "07e0",
        "svendor": "VMware",
        "svendor_id": "15ad",
        "sdevice": "SATA AHCI controller",
        "sdevice_id": "07e0",
        "physlot": "37",
        "progif": "01"
      },
      ...
    ]

<a id="jc.parsers.lspci.parse"></a>

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

Source: [`jc/parsers/lspci.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/lspci.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
