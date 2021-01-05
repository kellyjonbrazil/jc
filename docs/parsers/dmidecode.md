
# jc.parsers.dmidecode
jc - JSON CLI output utility `dmidecode` command output parser

Usage (cli):

    $ dmidecode | jc --dmidecode

    or

    $ jc dmidecode

Usage (module):

    import jc.parsers.dmidecode
    result = jc.parsers.dmidecode.parse(dmidecode_command_output)

Compatibility:

    'linux'

Examples:

    # dmidecode | jc --dmidecode -p
    [
      {
        "handle": "0x0000",
        "type": 0,
        "bytes": 24,
        "description": "BIOS Information",
        "values": {
          "vendor": "Phoenix Technologies LTD",
          "version": "6.00",
          "release_date": "04/13/2018",
          "address": "0xEA490",
          "runtime_size": "88944 bytes",
          "rom_size": "64 kB",
          "characteristics": [
            "ISA is supported",
            "PCI is supported",
            "PC Card (PCMCIA) is supported",
            "PNP is supported",
            "APM is supported",
            "BIOS is upgradeable",
            "BIOS shadowing is allowed",
            "ESCD support is available",
            "Boot from CD is supported",
            "Selectable boot is supported",
            "EDD is supported",
            "Print screen service is supported (int 5h)",
            "8042 keyboard services are supported (int 9h)",
            "Serial services are supported (int 14h)",
            "Printer services are supported (int 17h)",
            "CGA/mono video services are supported (int 10h)",
            "ACPI is supported",
            "Smart battery is supported",
            "BIOS boot specification is supported",
            "Function key-initiated network boot is supported",
            "Targeted content distribution is supported"
          ],
          "bios_revision": "4.6",
          "firmware_revision": "0.0"
        }
      },
      ...
    ]

    # dmidecode | jc --dmidecode -p -r
    [
      {
        "handle": "0x0000",
        "type": "0",
        "bytes": "24",
        "description": "BIOS Information",
        "values": {
          "vendor": "Phoenix Technologies LTD",
          "version": "6.00",
          "release_date": "04/13/2018",
          "address": "0xEA490",
          "runtime_size": "88944 bytes",
          "rom_size": "64 kB",
          "characteristics": [
            "ISA is supported",
            "PCI is supported",
            "PC Card (PCMCIA) is supported",
            "PNP is supported",
            "APM is supported",
            "BIOS is upgradeable",
            "BIOS shadowing is allowed",
            "ESCD support is available",
            "Boot from CD is supported",
            "Selectable boot is supported",
            "EDD is supported",
            "Print screen service is supported (int 5h)",
            "8042 keyboard services are supported (int 9h)",
            "Serial services are supported (int 14h)",
            "Printer services are supported (int 17h)",
            "CGA/mono video services are supported (int 10h)",
            "ACPI is supported",
            "Smart battery is supported",
            "BIOS boot specification is supported",
            "Function key-initiated network boot is supported",
            "Targeted content distribution is supported"
          ],
          "bios_revision": "4.6",
          "firmware_revision": "0.0"
        }
      },
      ...
    ]


## info
```python
info()
```


## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (List of Dictionaries) raw structured data to process

Returns:

    List of Dictionaries. Structured data with the following schema:

    [
      {
        "handle":                      string,
        "type":                        integer,
        "bytes":                       integer,
        "description":                 string,
        "values": {                               (null if empty)
          "lowercase_no_spaces_keys":  string,
          "multiline_key_values": [
                                       string,
          ]
        }
      }
    ]


## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

