import json
import re
import unittest

from jc.parsers.bluetoothctl import (
    _controller_head_pattern,
    _controller_line_pattern,
    _device_head_pattern,
    _device_line_pattern,
    _parse_controller,
    _parse_device,
    Controller,
    Device,
    parse,
)


class BluetoothctlTests(unittest.TestCase):
    def test_bluetoothctl_nodata(self):
        """
        Test 'bluetoothctl' with no data
        """

        output=''
        self.assertEqual(parse(output, quiet=True), [])

    def test_bluetoothctl_invalid_call(self):
        """
        Test 'bluetoothctl' with output from invalid call
        """

        output='Invalid command in menu main: foo'
        self.assertEqual(parse(output, quiet=True), [])

    def test_bluetoothctl_with_invalid_args(self):
        """
        Test 'bluetoothctl' with output from invalid arguments
        """

        output='Too many arguments: 2 > 1'
        self.assertEqual(parse(output, quiet=True), [])

    def test_bluetoothctl_no_controller(self):
        """
        Test 'bluetoothctl' with no controller
        """

        output='No default controller available'
        self.assertEqual(parse(output, quiet=True), [])


    def test_bluetoothctl_no_controller_found(self):
        """
        Test 'bluetoothctl' with no controller found
        """

        output='Controller EB:06:EF:62:B3:33 not available'
        self.assertEqual(parse(output, quiet=True), [])

    def test_bluetoothctl_no_device_found(self):
        """
        Test 'bluetoothctl' with no device found
        """

        output='Device EB:06:EF:62:B3:33 not available'
        self.assertEqual(parse(output, quiet=True), [])

    def test_bluetoothctl_controller(self):
        """
        Test 'bluetoothctl' with controller
        """

        with open("tests/fixtures/generic/bluetoothctl_controller.out", "r") as f:
            output = f.read()

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])

        expected = {
            "address": "CC:BB:AF:27:6A:E4",
            "is_public": True,
            "name": "arch",
            "alias": "arch",
            "class": "0x006c010c",
            "powered": "yes",
            "discoverable": "no",
            "discoverable_timeout": "0x000000b4",
            "pairable": "no",
            "uuids": [
                "Handsfree                 (0000111e-0000-1000-8000-00805f9b34fb)",
                "Audio Source              (0000110a-0000-1000-8000-00805f9b34fb)",
                "Audio Sink                (0000110b-0000-1000-8000-00805f9b34fb)",
                "PnP Information           (00001200-0000-1000-8000-00805f9b34fb)",
                "A/V Remote Control Target (0000110c-0000-1000-8000-00805f9b34fb)",
                "A/V Remote Control        (0000110e-0000-1000-8000-00805f9b34fb)",
                "Handsfree Audio Gateway   (0000111f-0000-1000-8000-00805f9b34fb)"
            ],
            "modalias": "usb:v1D6Bp0246d0542",
            "discovering": "no"
        }

        if actual:
            for k, v in expected.items():
                self.assertEqual(v, actual[0][k], f"Controller regex failed on {k}")

    def test_bluetoothctl_controller_2(self):
        """
        Test 'bluetoothctl' with controller 2
        """

        with open("tests/fixtures/generic/bluetoothctl_controller_2.out", "r") as f:
            output = f.read()

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])

        expected = {
            "address": "CC:52:AF:17:6A:E4",
            "is_public": True,
            "name": "starbase",
            "alias": "starbase",
            "class": "0x006c010c (7078156)",
            "powered": "yes",
            "power_state": "on",
            "discoverable": "no",
            "discoverable_timeout": "0x000000b4 (180)",
            "pairable": "no",
            "uuids": [
                "Handsfree                 (0000111e-0000-1000-8000-00805f9b34fb)",
                "Audio Source              (0000110a-0000-1000-8000-00805f9b34fb)",
                "Audio Sink                (0000110b-0000-1000-8000-00805f9b34fb)",
                "PnP Information           (00001200-0000-1000-8000-00805f9b34fb)",
                "A/V Remote Control Target (0000110c-0000-1000-8000-00805f9b34fb)",
                "A/V Remote Control        (0000110e-0000-1000-8000-00805f9b34fb)",
                "Handsfree Audio Gateway   (0000111f-0000-1000-8000-00805f9b34fb)"
            ],
            "modalias": "usb:v1D6Bp0246d054F",
            "discovering": "no"
        }

        if actual:
            for k, v in expected.items():
                self.assertEqual(v, actual[0][k], f"Controller regex failed on {k}")

    def test_bluetoothctl_controller_with_manufacturer(self):
        """
        Test 'bluetoothctl' with controller having manufacturer attr
        """

        with open("tests/fixtures/generic/bluetoothctl_controller_with_manufacturer.out", "r") as f:
            output = f.read()

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])

        expected = {
            "manufacturer": "0x0002 (2)",
            "version": "0x08 (8)",
            "address": "48:A4:72:3C:96:63",
            "is_public": True,
            "name": "ubuntu",
            "alias": "ubuntu",
            "class": "0x007c0104 (8126724)",
            "powered": "yes",
            "discoverable": "yes",
            "discoverable_timeout": "0x000000b4 (180)",
            "pairable": "yes",
            "uuids": [
                "Message Notification Se.. (00001133-0000-1000-8000-00805f9b34fb)",
                "A/V Remote Control        (0000110e-0000-1000-8000-00805f9b34fb)",
                "OBEX Object Push          (00001105-0000-1000-8000-00805f9b34fb)",
                "Message Access Server     (00001132-0000-1000-8000-00805f9b34fb)",
                "PnP Information           (00001200-0000-1000-8000-00805f9b34fb)",
                "IrMC Sync                 (00001104-0000-1000-8000-00805f9b34fb)",
                "Vendor specific           (00005005-0000-1000-8000-0002ee000001)",
                "A/V Remote Control Target (0000110c-0000-1000-8000-00805f9b34fb)",
                "Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)",
                "Phonebook Access Server   (0000112f-0000-1000-8000-00805f9b34fb)",
                "Audio Sink                (0000110b-0000-1000-8000-00805f9b34fb)",
                "Device Information        (0000180a-0000-1000-8000-00805f9b34fb)",
                "Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)",
                "Handsfree Audio Gateway   (0000111f-0000-1000-8000-00805f9b34fb)",
                "Audio Source              (0000110a-0000-1000-8000-00805f9b34fb)",
                "OBEX File Transfer        (00001106-0000-1000-8000-00805f9b34fb)",
                "Handsfree                 (0000111e-0000-1000-8000-00805f9b34fb)"
            ],
            "modalias": "usb:v1D6Bp0246d0548",
            "discovering": "yes"
        }

        if actual:
            for k, v in expected.items():
                self.assertEqual(v, actual[0][k], f"Controller regex failed on {k}")

    def test_bluetoothctl_controllers(self):
        """
        Test 'bluetoothctl' with controllers
        """

        output='Controller CC:52:AF:A4:6A:E4 arch [default]\n'
        output+='Controller CC:53:AF:17:6A:34 logi'

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])
        self.assertIsNotNone(actual[1])

        expected = [
            {
                "address": "CC:52:AF:A4:6A:E4",
                "is_default": True,
                "name": "arch"
            },
            {
                "address": "CC:53:AF:17:6A:34",
                "name": "logi"
            },
        ]

        if actual:
            for k, v in expected[0].items():
                self.assertEqual(v, actual[0][k], f"Controller regex failed on {k}")

            for k, v in expected[1].items():
                self.assertEqual(v, actual[1][k], f"Controller regex failed on {k}")

    def test_bluetoothctl_device(self):
        """
        Test 'bluetoothctl' with device
        """

        with open("tests/fixtures/generic/bluetoothctl_device.out", "r") as f:
            output = f.read()

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])

        expected = {
            "address": "EB:06:EF:62:B3:19",
            "is_public": True,
            "name": "TaoTronics TT-BH026",
            "alias": "TaoTronics TT-BH026",
            "class": "0x00240404",
            "icon": "audio-headset",
            "paired": "no",
            "bonded": "no",
            "trusted": "no",
            "blocked": "no",
            "connected": "no",
            "legacy_pairing": "no",
            "uuids": [
                "Advanced Audio Distribu.. (0000110d-0000-1000-8000-00805f9b34fb)",
                "Audio Sink                (0000110b-0000-1000-8000-00805f9b34fb)",
                "A/V Remote Control        (0000110e-0000-1000-8000-00805f9b34fb)",
                "A/V Remote Control Cont.. (0000110f-0000-1000-8000-00805f9b34fb)",
                "Handsfree                 (0000111e-0000-1000-8000-00805f9b34fb)",
                "Headset                   (00001108-0000-1000-8000-00805f9b34fb)",
                "Headset HS                (00001131-0000-1000-8000-00805f9b34fb)"
            ],
            "rssi": -52,
            "txpower": 4
        }

        if actual:
            for k, v in expected.items():
                self.assertEqual(v, actual[0][k], f"Device regex failed on {k}")
    def test_bluetoothctl_device_with_battery(self):
        """
        Test 'bluetoothctl' with device that has a battery
        """

        with open("tests/fixtures/generic/bluetoothctl_device_with_battery.out", "r") as f:
            output = f.read()

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0], actual)

        expected = {
            "name": "WH-1000XM3",
            "is_public": True,
            "is_random": False,
            "address": "67:F6:B4:0E:5C:94",
            "alias": "WH-1000XM3",
            "appearance": "",
            "class": "0x11240404 (2360324)",
            "icon": "audio-headset",
            "paired": "yes",
            "bonded": "yes",
            "trusted": "yes",
            "blocked": "no",
            "connected": "yes",
            "legacy_pairing": "no",
            "rssi": 0,
            "txpower": 0,
            "uuids": [
                "Vendor specific           (fd096fad-eed7-4504-943b-5fa1c0e761b2)",
                "Vendor specific           (03c57488-f7b6-45a3-8a23-ed4a890075cd)",
                "Vendor specific           (77a369ae-e453-4ff7-bc84-dc8f411eaa6a)",
                "Vendor specific           (8c274bd0-e7bd-4ed0-a391-55465e38005c)"
            ],
            "modalias": "usb:v052Cp0DC3d1426",
            "battery_percentage": 70
        }
        
        if actual:
            for k, v in expected.items():
                self.assertEqual(v, actual[0][k], f"Device regex failed on {k}")

    def test_bluetoothctl_device_random(self):
        """
        Test 'bluetoothctl' with device random
        """

        with open("tests/fixtures/generic/bluetoothctl_device_random.out", "r") as f:
            output = f.read()

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])

        expected = {
            "address": "DF:1C:C3:B4:1A:1F",
            "is_random": True,
            "name": "M585/M590",
            "alias": "M585/M590",
            "appearance": "0x03c2",
            "icon": "input-mouse",
            "paired": "yes",
            "bonded": "yes",
            "trusted": "no",
            "blocked": "no",
            "connected": "no",
            "legacy_pairing": "no",
            "uuids": [
                "Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)",
                "Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)",
                "Device Information        (0000180a-0000-1000-8000-00805f9b34fb)",
                "Battery Service           (0000180f-0000-1000-8000-00805f9b34fb)",
                "Human Interface Device    (00001812-0000-1000-8000-00805f9b34fb)",
                "Vendor specific           (00010000-0000-1000-8000-011f2000046d)"
            ],
            "modalias": "usb:v046DpB01Bd0011"
        }

        if actual:
            for k, v in expected.items():
                self.assertEqual(v, actual[0][k], f"Device regex failed on {k}")

    def test_bluetoothctl_devices(self):
        """
        Test 'bluetoothctl' with devices
        """

        output='Device EB:06:EF:62:13:19 TaoTronics TT-BH026\n'
        output+='Device AC:1F:EA:F8:AA:A1 wacom'

        actual = parse(output, quiet=True)

        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])
        self.assertIsNotNone(actual[1])

        expected = [
            {
                "address": "EB:06:EF:62:13:19",
                "name": "TaoTronics TT-BH026"
            },
            {
                "address": "AC:1F:EA:F8:AA:A1",
                "name": "wacom"
            }
        ]

        if actual:
            for k, v in expected[0].items():
                self.assertEqual(v, actual[0][k], f"Device regex failed on {k}")

            for k, v in expected[1].items():
                self.assertEqual(v, actual[1][k], f"Device regex failed on {k}")


if __name__ == '__main__':
    unittest.main()
