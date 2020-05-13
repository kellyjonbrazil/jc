# jc.parsers.dmidecode
jc - JSON CLI output utility dmidecode Parser

Usage:

    specify --dmidecode as the first argument if the piped input is coming from dmidecode

    Note: Because the output of dmidecode has some quirks, there may (rarely) be some missing data.
          For example, with mixed single and multi-line items only the first item is output.

          this:
            Associated Memory Slots: 2
                0x0006
                0x0007

          is converted to:
            "associated_memory_slots": "2",

          Very rarely there is an item with multiple sub-items and descriptions. These items will
          become corrupted.

          this:
            Handle 0x019F, DMI type 10, 8 bytes
            On Board Device 1 Information
                    Type: Video
                    Status: Disabled
                    Description: VMware SVGA II
            On Board Device 2 Information
                    Type: Sound
                    Status: Disabled
                    Description: ES1371

          is converted to:
            {
                "handle": "0x019F",
                "type": 10,
                "bytes": 8,
                "description": "On Board Device 1 Information",
                "values": {
                  "type": "Sound",
                  "status": "Disabled",
                  "description": "ES1371"
            }

Compatibility:

    'linux'

Examples:

    $ dmidecode | jc --dmidecode -p
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

    $ dmidecode | jc --dmidecode -p -r
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
info(self, /, *args, **kwargs)
```

## process
```python
process(proc_data)
```

Final processing to conform to the schema.

Parameters:

    proc_data:   (dictionary) raw structured data to process

Returns:

    List of dictionaries. Structured data with the following schema:

    [
      {
        "handle":                      string,
        "type":                        integer,
        "bytes":                       integer,
        "description":                 string,
        "values": {
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

    List of dictionaries. Raw or processed structured data.

