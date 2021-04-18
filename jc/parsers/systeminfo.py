"""jc - JSON CLI output utility `systeminfo` command output parser

Blank or missing elements are set to `null`.

The `original_install_date_epoch` and `system_boot_time_epoch` calculated timestamp fields are naive (i.e. based on the local time of the system the parser is run on)

The `original_install_date_epoch_utc` and `system_boot_time_epoch_utc` calculated timestamp fields are timezone-aware and are only available if the timezone field is UTC.

Usage (cli):

    $ systeminfo | jc --systeminfo

Usage (module):

    import jc.parsers.systeminfo
    result = jc.parsers.systeminfo.parse(systeminfo_command_output)

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
      "original_install_date_epoch":                integer,     # naive timestamp
      "original_install_date_epoch_utc":            integer,     # timezone-aware timestamp
      "system_boot_time":                           string,
      "system_boot_time_epoch":                     integer,     # naive timestamp
      "system_boot_time_epoch_utc":                 integer,     # timezone-aware timestamp
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
"""
import re
import jc.utils


class info:
    """Provides parser metadata (version, author, etc.)"""
    version = "1.0"
    description = "`systeminfo` command parser"
    author = "Jon Smith"
    author_email = "jon@rebelliondefense.com"
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ["win32"]
    magic_commands = ["systeminfo"]


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Some keys are optional. Example: a system without hyper-v capabilities
        will not have a 'hyperv_requirements' key, and a system already running hyper-v
        will have an empty "hyperv_requirements" object.

        Structured data to conform to the schema.
    """
    # convert empty strings to None/null
    for item in proc_data:
        if isinstance(proc_data[item], str) and not proc_data[item]:
            proc_data[item] = None

    for i, nic in enumerate(proc_data["network_cards"]):
        proc_data["network_cards"][i]["dhcp_enabled"] = jc.utils.convert_to_bool(
            nic["dhcp_enabled"]
        )

        # convert empty strings to None/null
        for item in nic:
            if isinstance(nic[item], str) and not nic[item]:
                proc_data["network_cards"][i][item] = None

    int_list = [
        "total_physical_memory_mb",
        "available_physical_memory_mb",
        "virtual_memory_max_size_mb",
        "virtual_memory_available_mb",
        "virtual_memory_in_use_mb",
    ]
    for key in int_list:
        proc_data[key] = jc.utils.convert_to_int(proc_data[key])

    dt_list = ["original_install_date", "system_boot_time"]
    for key in dt_list:
        tz = proc_data.get("time_zone", "")
        if tz:
            # convert
            # from: (UTC-08:00) Pacific Time (US & Canada)
            # to: (UTC-0800)
            tz_fields = tz.split()
            tz = " " + tz_fields[0].replace(":", "")
        proc_data[key + '_epoch'] = jc.utils.timestamp(f"{proc_data.get(key)}{tz}").naive
        proc_data[key + '_epoch_utc'] = jc.utils.timestamp(f"{proc_data.get(key)}{tz}").utc

    hyperv_key = "hyperv_requirements"
    hyperv_subkey_list = [
        "vm_monitor_mode_extensions",
        "virtualization_enabled_in_firmware",
        "second_level_address_translation",
        "data_execution_prevention_available",
    ]
    if hyperv_key in proc_data:
        for key in hyperv_subkey_list:
            if key in proc_data[hyperv_key]:
                proc_data[hyperv_key][key] = jc.utils.convert_to_bool(
                    proc_data[hyperv_key][key]
                )

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    delim = ":"  # k/v delimiter
    raw_data = {}  # intermediary output

    if jc.utils.has_data(data):
        # keepends = True, so that multiline data retains return chars
        lines = [line for line in data.splitlines(keepends=True) if line.strip() != ""]

        # find the character position of the value in the k/v pair of the first line
        # all subsequent lines of data use the same character position
        start_value_pos = _get_value_pos(lines[0], delim)

        last_key = None
        for line in lines:
            key = line[0:start_value_pos]
            value = line[start_value_pos:]

            # possible multiline data
            if last_key:
                # the value data doesn't start where it should
                # so this is multiline data
                if delim not in key:
                    raw_data[last_key] += line
                    continue

            raw_data[key] = value
            last_key = key

    # clean up keys; strip values
    raw_output = {}
    for k, v in raw_data.items():
        k = _transform_key(k)

        # since we split on start_value_pos, the delimiter
        # is still in the key field. Remove it.
        k = k.rstrip(delim)

        if k in ["hotfixs", "processors"]:
            raw_output[k] = _parse_hotfixs_or_processors(v)
        elif k in ["network_cards"]:
            raw_output[k] = _parse_network_cards(v)
        elif k in ["hyperv_requirements"]:
            raw_output[k] = _parse_hyperv_requirements(v)
        elif k in [
            "total_physical_memory",
            "available_physical_memory",
            "virtual_memory_max_size",
            "virtual_memory_available",
            "virtual_memory_in_use"
        ]:
            raw_output[k + "_mb"] = v.strip()
        else:
            raw_output[k] = v.strip()

    if raw:
        return raw_output
    else:
        return _process(raw_output)


def _parse_hotfixs_or_processors(data):
    """
    Turns a list of return-delimited hotfixes or processors
    with [x] as a prefix into an array of hotfixes

    Note that if a high number of items exist, the list may cutoff
    and this list may not contain all items installed on the system

    IRL, this likely applies to hotfixes more than processors

    Parameters:
        data: (string) Input string
    """
    arr_output = []
    for i, l in enumerate(data.splitlines()):
        # skip line that says how many are installed
        if i == 0:
            continue
        # we have to make sure this is a complete line
        # as data could cutoff. Make sure the delimiter
        # exists. Otherwise, skip it.
        if ":" in l:
            k, v = l.split(":")
            # discard the number sequence
            arr_output.append(v.strip())

    return arr_output


def _parse_hyperv_requirements(data):
    """
    Turns a list of key/value settings for hyperv
    into an object

    Parameters:
        data: (string) Input string
    """
    output = {}
    for i, l in enumerate(data.splitlines()):
        if ":" in l:
            k, v = l.split(":")
            # discard the number sequence
            output[_transform_key(k)] = v.strip()

    return output


def _parse_network_cards(data):
    """
    Turns a list of network_cards into an array of objects

    Parameters:
        data: (string) Input string
    """
    delim = ":"
    arr_output = []
    cur_nic = None
    is_ip = False
    nic_value_pos = 0

    for i, line in enumerate(data.splitlines()):
        # skip first line
        if i == 0:
            continue

        if "IP address(es)" in line:
            is_ip = True
            continue

        cur_value_pos = len(line) - len(line.lstrip())

        line = line.strip()

        m = re.match(r"\[(\d+)\]" + delim + "(.+)", line)
        if m and is_ip and cur_value_pos > nic_value_pos:
            cur_nic["ip_addresses"].append(m.group(2).strip())
        elif m:
            if cur_nic:
                arr_output.append(cur_nic)
            cur_nic = _default_nic()
            cur_nic["name"] = m.group(2).strip()
            nic_value_pos = cur_value_pos
            is_ip = False
        elif delim in line:
            k, v = line.split(delim)
            k = _transform_key(k)
            cur_nic[k] = v.strip()

    if cur_nic:
        arr_output.append(cur_nic)

    return arr_output


def _convert_to_boolean(value):
    """
    Converts string input to boolean assuming "Yes/No" inputs

    Parameters:
        value: (string) Input value
    """
    return value == "Yes"


def _convert_to_int(value):
    """
    Converts string input to integer by stripping all non-numeric characters

    Parameters:
        value: (string) Input value
    """
    try:
        value = int(re.sub("[^0-9]", "", value))
    except ValueError:
        pass
    return value


def _default_nic():
    """
    Returns a default network card object
    """
    return {
        "name": "",
        "connection_name": "",
        "status": "",
        "dhcp_enabled": "No",
        "dhcp_server": "",
        "ip_addresses": [],
    }


def _get_value_pos(line, delim):
    """
    Finds the first non-whitespace character after the delimiter

    Parameters:
        line: (string) Input string
        delim: (string) The data delimiter
    """
    fields = line.split(delim, 1)
    if not len(fields) == 2:
        raise Exception(f"Expected a '{delim}' delimited field. Actual: {line}")

    return len(line) - len(fields[1].lstrip())


def _transform_key(key):
    """
    Converts a given key to a valid json key that plays nice with jq

    Parameters:
        key: (string) Input value
    """
    # lowercase and replace spaces with underscores
    key = key.strip().lower().replace(" ", "_")

    # remove invalid key characters
    for c in ";:!@#$%^&*()-":
        key = key.replace(c, "")
    return key
