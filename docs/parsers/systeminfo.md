[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.systeminfo"></a>

# jc.parsers.systeminfo

jc - JSON Convert `systeminfo` command output parser

Blank or missing elements are set to `null`.

The `original_install_date_epoch` and `system_boot_time_epoch` calculated
timestamp fields are naive. (i.e. based on the local time of the system the
parser is run on)

The `original_install_date_epoch_utc` and `system_boot_time_epoch_utc`
calculated timestamp fields are timezone-aware and are only available if
the timezone field is UTC.

Usage (cli):

    $ systeminfo | jc --systeminfo

Usage (module):

    import jc
    result = jc.parse('systeminfo', systeminfo_command_output)

Schema:

    {
      "host_name":                                  string,
      "os_name":                                    string,
      "os_version":                                 string,
      "os_manufacturer":                            string,
      "os_configuration":                           string,
      "os_build_type":                              string,
      "registered_owner":                           string,
      "registered_organization":                    string,
      "product_id":                                 string,
      "original_install_date":                      string,
      "original_install_date_epoch":                integer,     # [0]
      "original_install_date_epoch_utc":            integer,     # [1]
      "system_boot_time":                           string,
      "system_boot_time_epoch":                     integer,     # [0]
      "system_boot_time_epoch_utc":                 integer,     # [1]
      "system_manufacturer":                        string,
      "system_model":                               string,
      "system_type":                                string,
      "processors": [
                                                    string
      ],
      "bios_version":                               string,
      "windows_directory":                          string,
      "system_directory":                           string,
      "boot_device":                                string,
      "system_locale":                              string,
      "input_locale":                               string,
      "time_zone":                                  string,
      "total_physical_memory_mb":                   string,
      "available_physical_memory_mb":               integer,
      "virtual_memory_max_size_mb":                 integer,
      "virtual_memory_available_mb":                integer,
      "virtual_memory_in_use_mb":                   integer,
      "page_file_locations":                        string,
      "domain":                                     string,
      "logon_server":                               string,
      "hotfixs": [
                                                    string
      ],
      "network_cards": [
        {
          "name":                                   string,
          "connection_name":                        string,
          "status":                                 string,
          "dhcp_enabled":                           boolean,
          "dhcp_server":                            string,
          "ip_addresses": [
                                                    string
          ]
        }
      ],
      "hyperv_requirements": {
        "vm_monitor_mode_extensions":               boolean,
        "virtualization_enabled_in_firmware":       boolean,
        "second_level_address_translation":         boolean,
        "data_execution_prevention_available":      boolean
      }
    }

    [0] naive timestamp
    [1] timezone-aware timestamp

Examples:

    $ systeminfo | jc --systeminfo -p
    {
      "host_name": "TESTLAPTOP",
      "os_name": "Microsoft Windows 10 Enterprise",
      "os_version": "10.0.17134 N/A Build 17134",
      "os_manufacturer": "Microsoft Corporation",
      "os_configuration": "Member Workstation",
      "os_build_type": "Multiprocessor Free",
      "registered_owner": "Test, Inc.",
      "registered_organization": "Test, Inc.",
      "product_id": "11111-11111-11111-AA111",
      "original_install_date": "3/26/2019, 3:51:30 PM",
      "system_boot_time": "3/30/2021, 6:13:59 AM",
      "system_manufacturer": "Dell Inc.",
      "system_model": "Precision 5530",
      "system_type": "x64-based PC",
      "processors": [
        "Intel64 Family 6 Model 158 Stepping 10 GenuineIntel ~2592 Mhz"
      ],
      "bios_version": "Dell Inc. 1.16.2, 4/21/2020",
      "windows_directory": "C:\\WINDOWS",
      "system_directory": "C:\\WINDOWS\\system32",
      "boot_device": "\\Device\\HarddiskVolume2",
      "system_locale": "en-us;English (United States)",
      "input_locale": "en-us;English (United States)",
      "time_zone": "(UTC+00:00) UTC",
      "total_physical_memory_mb": 32503,
      "available_physical_memory_mb": 19743,
      "virtual_memory_max_size_mb": 37367,
      "virtual_memory_available_mb": 22266,
      "virtual_memory_in_use_mb": 15101,
      "page_file_locations": "C:\\pagefile.sys",
      "domain": "test.com",
      "logon_server": "\\\\TESTDC01",
      "hotfixs": [
        "KB2693643",
        "KB4601054"
      ],
      "network_cards": [
        {
          "name": "Intel(R) Wireless-AC 9260 160MHz",
          "connection_name": "Wi-Fi",
          "status": null,
          "dhcp_enabled": true,
          "dhcp_server": "192.168.2.1",
          "ip_addresses": [
            "192.168.2.219"
          ]
        }
      ],
      "hyperv_requirements": {
        "vm_monitor_mode_extensions": true,
        "virtualization_enabled_in_firmware": true,
        "second_level_address_translation": false,
        "data_execution_prevention_available": true
      },
      "original_install_date_epoch": 1553640690,
      "original_install_date_epoch_utc": 1553615490,
      "system_boot_time_epoch": 1617110039,
      "system_boot_time_epoch_utc": 1617084839
    }

    $ systeminfo | jc --systeminfo -p -r
    {
      "host_name": "TESTLAPTOP",
      "os_name": "Microsoft Windows 10 Enterprise",
      "os_version": "10.0.17134 N/A Build 17134",
      "os_manufacturer": "Microsoft Corporation",
      "os_configuration": "Member Workstation",
      "os_build_type": "Multiprocessor Free",
      "registered_owner": "Test, Inc.",
      "registered_organization": "Test, Inc.",
      "product_id": "11111-11111-11111-AA111",
      "original_install_date": "3/26/2019, 3:51:30 PM",
      "system_boot_time": "3/30/2021, 6:13:59 AM",
      "system_manufacturer": "Dell Inc.",
      "system_model": "Precision 5530",
      "system_type": "x64-based PC",
      "processors": [
        "Intel64 Family 6 Model 158 Stepping 10 GenuineIntel ~2592 Mhz"
      ],
      "bios_version": "Dell Inc. 1.16.2, 4/21/2020",
      "windows_directory": "C:\\WINDOWS",
      "system_directory": "C:\\WINDOWS\\system32",
      "boot_device": "\\Device\\HarddiskVolume2",
      "system_locale": "en-us;English (United States)",
      "input_locale": "en-us;English (United States)",
      "time_zone": "(UTC+00:00) UTC",
      "total_physical_memory_mb": "32,503 MB",
      "available_physical_memory_mb": "19,743 MB",
      "virtual_memory_max_size_mb": "37,367 MB",
      "virtual_memory_available_mb": "22,266 MB",
      "virtual_memory_in_use_mb": "15,101 MB",
      "page_file_locations": "C:\\pagefile.sys",
      "domain": "test.com",
      "logon_server": "\\\\TESTDC01",
      "hotfixs": [
        "KB2693643",
        "KB4601054"
      ],
      "network_cards": [
        {
          "name": "Intel(R) Wireless-AC 9260 160MHz",
          "connection_name": "Wi-Fi",
          "status": "",
          "dhcp_enabled": "Yes",
          "dhcp_server": "192.168.2.1",
          "ip_addresses": [
            "192.168.2.219"
          ]
        }
      ],
      "hyperv_requirements": {
        "vm_monitor_mode_extensions": "Yes",
        "virtualization_enabled_in_firmware": "Yes",
        "second_level_address_translation": "No",
        "data_execution_prevention_available": "Yes"
      }
    }

<a id="jc.parsers.systeminfo.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  win32

Source: [`jc/parsers/systeminfo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/systeminfo.py)

Version 1.3 by Jon Smith (jon@rebelliondefense.com)
