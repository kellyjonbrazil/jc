
# jc.parsers.systeminfo
jc - JSON CLI output utility `systeminfo` command output parser

Parses Windows "systeminfo" command. Multiline values such as
hotfixes or network cards are unparsed.

Usage (cli):

    $ systeminfo | jc --systeminfo

Usage (module):

    import jc.parsers.systeminfo
    result = jc.parsers.systeminfo.parse(systeminfo_command_output)

Compatibility:

    'win32'

Examples:

    $ systeminfo | jc --systeminfo -p
    {
        "host_name": "DESKTOP-WIN01",
        "os_name": "Microsoft Windows 10 Enterprise",
        "os_version": "10.0.19042 N/A Build 19042",
        "os_manufacturer": "Microsoft Corporation",
        "os_configuration": "Member Workstation",
        "os_build_type": "Multiprocessor Free",
        "registered_owner": "User",
        "registered_organization": "",
        "product_id": "00111-12345-00001-AA111",
        "original_install_date": "2/16/2021, 11:20:27 AM",
        "system_boot_time": "3/19/2021, 9:25:03 AM",
        "system_manufacturer": "VMware, Inc.",
        "system_model": "VMware7,1",
        "system_type": "x64-based PC",
        "processors": "1 Processor(s) Installed.
                           [01]: ...",
        "bios_version": "VMware, Inc. VMW71.00V.11111111.B64.2008100111, 8/10/2020",
        "windows_directory": "C:\Windows",
        "system_directory": "C:\Windows\system32",
        "boot_device": "\Device\HarddiskVolume1",
        "system_locale": "en-us;English (United States)",
        "input_locale": "en-us;English (United States)",
        "time_zone": "(UTC-08:00) Pacific Time (US & Canada)",
        "total_physical_memory": "2,047 MB",
        "available_physical_memory": "1,417 MB",
        "virtual_memory_max_size": "2,687 MB",
        "virtual_memory_available": "1,482 MB",
        "virtual_memory_in_use": "1,205 MB",
        "page_file_locations": "C:\pagefile.sys",
        "domain": "TEST.local",
        "logon_server": "\\WIN-AA1A1A11AAA",
        "hotfixs": "6 Hotfix(s) Installed.
                           [01]: KB4578...",
        "network_cards": "1 NIC(s) Installed.
                           [01]: Int...",
        "hyperv_requirements": "A hypervisor has been detected. Features required fo..."
    }


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

    List of Dictionaries. Some keys are optional. Example: a non-virtualized server will not have
    the "hyperv_requirements" key. Structured data with the following schema:

    [
        {
            "host_name": "string",
            "os_name": "string",
            "os_version": "string",
            "os_manufacturer": "string",
            "os_configuration": "string",
            "os_build_type": "string",
            "registered_owner": "string",
            "registered_organization": "string",
            "product_id": "string",
            "original_install_date": "string",
            "system_boot_time": "string",
            "system_manufacturer": "string",
            "system_model": "string",
            "system_type": "string",
            "processors": "string",
            "bios_version": "string",
            "windows_directory": "string",
            "system_directory": "string",
            "boot_device": "string",
            "system_locale": "string",
            "input_locale": "string",
            "time_zone": "string",
            "total_physical_memory": "string",
            "available_physical_memory": "string",
            "virtual_memory_max_size": "string",
            "virtual_memory_available": "string",
            "virtual_memory_in_use": "string",
            "page_file_locations": "string",
            "domain": "string",
            "logon_server": "string",
            "hotfixs": "string",
            "network_cards": "string",
            "hyperv_requirements": "string"
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


## get_value_pos
```python
get_value_pos(line, delim)
```

Finds the first non-whitespace character after the delimiter
Parameters:
    line: (string) Input string
    delim: (string) The data delimiter

