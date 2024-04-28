r"""jc - JSON Convert `pci.ids` file parser

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
"""
import re
from typing import Dict
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`pci.ids` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['file']


__version__ = info.version


def _process(proc_data: JSONDictType) -> JSONDictType:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> JSONDictType:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}
    vdc_obj: Dict = {}
    vendor_id: str = ''
    device_id: str = ''

    class_obj: Dict = {}
    class_id: str = ''
    subclass_id: str = ''

    if jc.utils.has_data(data):

        vdc_header_p = re.compile(r'^(?P<vendor_id>[0-9a-f]{4})\s+(?P<vendor_name>.+)')
        vdc_device_p = re.compile(r'^\t(?P<device_id>[0-9a-f]{4})\s+(?P<device_name>.+)')
        vdc_subvendor_p = re.compile(r'^\t\t(?P<subvendor>[0-9a-f]{4})\s+(?P<subdevice>[0-9a-f]{4})\s+(?P<subsystem_name>.+)')

        class_header_p = re.compile(r'^C\s+(?P<class_id>[0-9a-f]{2})\s+(?P<class_name>.+)')
        class_sub_p = re.compile(r'^\t(?P<subclass_id>[0-9a-f]{2})\s+(?P<subclass_name>.+)')
        class_progif_p = re.compile(r'^\t\t(?P<prog_if_id>[0-9a-f]{2})\s+(?P<prog_if_name>.+)')

        for line in filter(None, data.splitlines()):

            vdc_header = vdc_header_p.match(line)
            vdc_device = vdc_device_p.match(line)
            vdc_subvendor = vdc_subvendor_p.match(line)

            class_header = class_header_p.match(line)
            class_sub = class_sub_p.match(line)
            class_progif = class_progif_p.match(line)

            # Vendors, devices and subsystems
            # Syntax:
            # vendor  vendor_name
            #	device  device_name                       <-- single tab
            #		subvendor subdevice  subsystem_name   <-- two tabs
            # Example:
            # 001c  PEAK-System Technik GmbH
            #     0001  PCAN-PCI CAN-Bus controller
            #         001c 0004  2 Channel CAN Bus SJC1000
            if vdc_header:
                if vdc_obj:
                    if 'vendors' not in raw_output:
                        raw_output['vendors'] = {}
                    raw_output['vendors'][vendor_id] = vdc_obj[vendor_id]
                    vdc_obj = {}

                vendor_id = '_' + vdc_header.groupdict()['vendor_id']
                vdc_obj[vendor_id] = {}
                vdc_obj[vendor_id]['vendor_name'] = vdc_header.groupdict()['vendor_name']
                continue

            if vdc_device:
                device_id = '_' + vdc_device.groupdict()['device_id']
                vdc_obj[vendor_id][device_id] = {}
                vdc_obj[vendor_id][device_id]['device_name'] = vdc_device.groupdict()['device_name']
                continue

            if vdc_subvendor:
                subvendor = '_' + vdc_subvendor.groupdict()['subvendor']
                subdevice = '_' + vdc_subvendor.groupdict()['subdevice']
                if not vdc_obj[vendor_id][device_id].get(subvendor) or not isinstance(vdc_obj[vendor_id][device_id][subvendor], dict):
                    vdc_obj[vendor_id][device_id][subvendor] = {}
                vdc_obj[vendor_id][device_id][subvendor][subdevice] = {}
                vdc_obj[vendor_id][device_id][subvendor][subdevice]['subsystem_name'] = vdc_subvendor.groupdict()['subsystem_name']
                continue

            # List of known device classes, subclasses and programming interfaces
            # Syntax:
            # C class	class_name
            #	subclass	subclass_name       <-- single tab
            #		prog-if  prog-if_name       <-- two tabs
            # Example:
            # C 01  Mass storage controller
            #     01  IDE interface
            #         00  ISA Compatibility mode-only controller
            if class_header:
                if class_obj:
                    if 'classes' not in raw_output:
                        raw_output['classes'] = {}
                    raw_output['classes'][class_id] = class_obj[class_id]
                    class_obj = {}

                class_id = '_' + class_header.groupdict()['class_id']
                class_obj[class_id] = {}
                class_obj[class_id]['class_name'] = class_header.groupdict()['class_name']
                continue

            if class_sub:
                subclass_id = '_' + class_sub.groupdict()['subclass_id']
                class_obj[class_id][subclass_id] = {}
                class_obj[class_id][subclass_id]['subclass_name'] = class_sub.groupdict()['subclass_name']
                continue

            if class_progif:
                prog_if_id = '_' + class_progif.groupdict()['prog_if_id']
                class_obj[class_id][subclass_id][prog_if_id] = class_progif.groupdict()['prog_if_name']
                continue

        if vdc_obj:
            if 'vendors' not in raw_output:
                raw_output['vendors'] = {}
            raw_output['vendors'][vendor_id] = vdc_obj[vendor_id]

        if class_obj:
            if 'classes' not in raw_output:
                raw_output['classes'] = {}
            raw_output['classes'][class_id] = class_obj[class_id]

    return raw_output if raw else _process(raw_output)
