import pprint
import json
import re
import unittest
from typing import Optional

from jc.parsers.xrandr import (
    Device,
    Edid,
    _Line,
    LineType,
    ResolutionMode,
    Response,
    Screen,
    _device_pattern,
    _frequencies_pattern,
    _parse_device,
    _parse_resolution_mode,
    _parse_screen,
    _resolution_mode_pattern,
    _screen_pattern,
    parse,
)


class XrandrTests(unittest.TestCase):
    def test_xrandr_nodata(self):
        """
        Test 'xrandr' with no data
        """
        self.assertEqual(parse("", quiet=True), {"screens": []})

    def test_regexes(self):
        devices = [
            "HDMI1 connected (normal left inverted right x axis y axis)",
            "VIRTUAL1 disconnected (normal left inverted right x axis y axis)",
            "eDP1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 310mm x 170mm",
            "eDP-1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 309mm x 174mm",
            "HDMI-0 connected 2160x3840+3840+0 right (normal left inverted right x axis y axis) 609mm x 349mm",
            "LVDS-1 connected primary 1366x768+0+0 normal X axis (normal left inverted right x axis y axis) 609mm x 349mm",
            "VGA-1 connected 1280x1024+0+0 left X and Y axis (normal left inverted right x axis y axis) 609mm x 349mm",
        ]
        for device in devices:
            self.assertIsNotNone(re.match(_device_pattern, device))

        screens = [
            "Screen 0: minimum 8 x 8, current 1920 x 1080, maximum 32767 x 32767",
            "Screen 0: minimum 320 x 200, current 1920 x 1080, maximum 16384 x 16384",
        ]
        for screen in screens:
            self.assertIsNotNone(re.match(_screen_pattern, screen))

        modes = [
            "1920x1080     60.03*+  59.93",
            "1680x1050     59.88",
            "1400x1050     59.98",
            "1600x900      60.00    59.95    59.82",
            "1280x1024     60.02",
            "1400x900      59.96    59.88",
        ]
        for mode in modes:
            match = re.match(_resolution_mode_pattern, mode)
            self.assertIsNotNone(match)
            if match:
                rest = match.groupdict()["rest"]
                self.assertIsNotNone(re.match(_frequencies_pattern, rest))

    def test_line_categorize(self):
        base = "eDP-1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 309mm x 174mm"
        resolution_mode = "   320x240       60.05"
        prop_key = "	EDID:"
        prop_value = "		00ffffffffffff0006af3d5700000000"
        invalid = ""

        self.assertEqual(LineType.Device, _Line.categorize(base).t)
        self.assertEqual(LineType.ResolutionMode, _Line.categorize(resolution_mode).t)
        self.assertEqual(LineType.PropKey, _Line.categorize(prop_key).t)
        self.assertEqual(LineType.PropValue, _Line.categorize(prop_value).t)
        with self.assertRaises(Exception):
            _Line.categorize(invalid)

    def test_screens(self):
        sample = "Screen 0: minimum 8 x 8, current 1920 x 1080, maximum 32767 x 32767"
        line = _Line.categorize(sample)
        actual: Optional[Screen] = _parse_screen(line)
        self.assertIsNotNone(actual)

        expected = {
            "screen_number": 0,
            "minimum_width": 8,
            "minimum_height": 8,
            "current_width": 1920,
            "current_height": 1080,
            "maximum_width": 32767,
            "maximum_height": 32767,
        }
        if actual:
            for k, v in expected.items():
                self.assertEqual(v, actual[k], f"screens regex failed on {k}")

        sample = (
            "Screen 0: minimum 320 x 200, current 1920 x 1080, maximum 16384 x 16384"
        )
        line = _Line.categorize(sample)
        actual = _parse_screen(line)
        if actual:
            self.assertEqual(320, actual["minimum_width"])
        else:
            raise AssertionError("Screen should not be None")

    def test_device(self):
        # regex101 sample link for tests/edits https://regex101.com/r/3cHMv3/1
        sample = "eDP1 connected primary 1920x1080+0+0 left (normal left inverted right x axis y axis) 310mm x 170mm"
        line = _Line.categorize(sample)
        actual: Optional[Device] = _parse_device(line)

        expected = {
            "device_name": "eDP1",
            "is_connected": True,
            "is_primary": True,
            "resolution_width": 1920,
            "resolution_height": 1080,
            "offset_width": 0,
            "offset_height": 0,
            "dimension_width": 310,
            "dimension_height": 170,
            "rotation": "left",
        }

        self.assertIsNotNone(actual)

        if actual:
            for k, v in expected.items():
                self.assertEqual(v, actual[k], f"Devices regex failed on {k}")

        # with open("tests/fixtures/generic/xrandr_device.out", "r") as f:
        #     extended_sample = f.read().splitlines()

        # device = _parse_device(extended_sample)
        # if device:
        #     self.assertEqual(
        #         59.94, device["resolution_modes"][12]["frequencies"][4]["frequency"]
        #     )

    def test_device_with_reflect(self):
        sample = "VGA-1 connected primary 1920x1080+0+0 left X and Y axis (normal left inverted right x axis y axis) 310mm x 170mm"
        line = _Line.categorize(sample)
        actual: Optional[Device] = _parse_device(line)

        expected = {
            "device_name": "VGA-1",
            "is_connected": True,
            "is_primary": True,
            "resolution_width": 1920,
            "resolution_height": 1080,
            "offset_width": 0,
            "offset_height": 0,
            "dimension_width": 310,
            "dimension_height": 170,
            "rotation": "left",
            "reflection": "X and Y axis",
        }

        self.assertIsNotNone(actual)

        if actual:
            for k, v in expected.items():
                self.assertEqual(v, actual[k], f"Devices regex failed on {k}")

    def test_mode(self):
        sample_1 = "   1920x1080     60.03*+  59.93"
        expected = {
            "frequencies": [
                {"frequency": 60.03, "is_current": True, "is_preferred": True},
                {"frequency": 59.93, "is_current": False, "is_preferred": False},
            ],
            "resolution_width": 1920,
            "resolution_height": 1080,
            "is_high_resolution": False,
        }
        line = _Line.categorize(sample_1)
        actual: Optional[ResolutionMode] = _parse_resolution_mode(line)

        self.assertIsNotNone(actual)

        if actual:
            for k, v in expected.items():
                self.assertEqual(v, actual[k], f"mode regex failed on {k}")

        sample_2 = "   1920x1080i    60.00    50.00    59.94"
        line = _Line.categorize(sample_2)
        actual: Optional[ResolutionMode] = _parse_resolution_mode(line)
        self.assertIsNotNone(actual)
        if actual:
            self.assertEqual(True, actual["is_high_resolution"])
            self.assertEqual(50.0, actual["frequencies"][1]["frequency"])

    def test_complete_1(self):
        self.maxDiff = None
        with open("tests/fixtures/generic/xrandr.out", "r") as f:
            actual = parse(f.read(), quiet=True)

        with open('tests/fixtures/generic/xrandr.json', 'r') as f:
            reference = json.loads(f.read())

        self.assertEqual(1, len(actual["screens"]))
        self.assertEqual(
            18, len(actual["screens"][0]["devices"][0]["resolution_modes"])
        )
        self.assertEqual(actual, reference)

    def test_complete_2(self):
        with open("tests/fixtures/generic/xrandr_2.out", "r") as f:
            actual = parse(f.read(), quiet=True)

        with open('tests/fixtures/generic/xrandr_2.json', 'r') as f:
            reference = json.loads(f.read())

        self.assertEqual(1, len(actual["screens"]))
        self.assertEqual(
            38, len(actual["screens"][0]["devices"][0]["resolution_modes"])
        )
        self.assertEqual(actual, reference)

    def test_complete_3(self):
        with open("tests/fixtures/generic/xrandr_3.out", "r") as f:
            actual = parse(f.read(), quiet=True)

        with open('tests/fixtures/generic/xrandr_3.json', 'r') as f:
            reference = json.loads(f.read())

        self.assertEqual(1, len(actual["screens"]))
        self.assertEqual(
            2,
            len(actual["screens"][0]["devices"]),
        )
        self.assertEqual(actual, reference)

    def test_complete_4(self):
        with open("tests/fixtures/generic/xrandr_simple.out", "r") as f:
            actual = parse(f.read(), quiet=True)

        with open('tests/fixtures/generic/xrandr_simple.json', 'r') as f:
            reference = json.loads(f.read())

        self.assertEqual(1, len(actual["screens"]))
        self.assertEqual(2, len(actual["screens"][0]["devices"][0]["resolution_modes"]))
        self.assertEqual(actual, reference)

    def test_complete_5(self):
        with open("tests/fixtures/generic/xrandr_properties_1.out", "r") as f:
            actual = parse(f.read(), quiet=True)

        with open('tests/fixtures/generic/xrandr_properties_1.json', 'r') as f:
            reference = json.loads(f.read())

        self.assertEqual(1, len(actual["screens"]))
        self.assertEqual(
            38, len(actual["screens"][0]["devices"][0]["resolution_modes"])
        )
        self.assertEqual(actual, reference)

    # def test_model(self):
    #     asus_edid = [
    #         "   EDID: ",
    #         "         00ffffffffffff000469d41901010101",
    #         "         2011010308291a78ea8585a6574a9c26",
    #         "         125054bfef80714f8100810f81408180",
    #         "         9500950f01019a29a0d0518422305098",
    #         "         360098ff1000001c000000fd00374b1e",
    #         "         530f000a202020202020000000fc0041",
    #         "         535553205657313933530a20000000ff",
    #         "         0037384c383032313130370a20200077",
    #     ]
    #     asus_edid.reverse()

    #     expected = {
    #         "name": "ASUS VW193S",
    #         "product_id": "6612",
    #         "serial_number": "78L8021107",
    #     }

    #     actual: Optional[EdidModel] = _parse_model(asus_edid)
    #     self.assertIsNotNone(actual)

    #     if actual:
    #         for k, v in expected.items():
    #             self.assertEqual(v, actual[k], f"mode regex failed on {k}")

    #     generic_edid = [
    #         "   EDID: ",
    #         "         00ffffffffffff004ca3523100000000",
    #         "         0014010380221378eac8959e57549226",
    #         "         0f505400000001010101010101010101",
    #         "         010101010101381d56d4500016303020",
    #         "         250058c2100000190000000f00000000",
    #         "         000000000025d9066a00000000fe0053",
    #         "         414d53554e470a204ca34154000000fe",
    #         "         004c544e313536415432343430310018",
    #     ]
    #     generic_edid.reverse()

    #     expected = {
    #         "name": "Generic",
    #         "product_id": "12626",
    #         "serial_number": "0",
    #     }

    #     jc.parsers.xrandr.parse_state = {}
    #     actual: Optional[EdidModel] = _parse_model(generic_edid)
    #     self.assertIsNotNone(actual)

    #     if actual:
    #         for k, v in expected.items():
    #             self.assertEqual(v, actual[k], f"mode regex failed on {k}")

    #     empty_edid = [""]
    #     actual: Optional[EdidModel] = _parse_model(empty_edid)
    #     self.assertIsNone(actual)

    def test_issue_490(self):
        """test for issue 490: https://github.com/kellyjonbrazil/jc/issues/490"""
        data_in = """\
Screen 0: minimum 1024 x 600, current 1024 x 600, maximum 1024 x 600
default connected 1024x600+0+0 0mm x 0mm
   1024x600 0.00*
"""
        actual: Response = parse(data_in, quiet=True)
        self.maxDiff = None
        self.assertEqual(1024, actual["screens"][0]["devices"][0]["resolution_width"])

    def test_issue_525(self):
        self.maxDiff = None
        with open("tests/fixtures/generic/xrandr_issue_525.out", "r") as f:
            txt = f.read()
        actual = parse(txt, quiet=True)
        dp4 = actual["screens"][0]["devices"][0]["props"]["Broadcast RGB"][1]  # type: ignore
        # pprint.pprint(actual)
        self.assertEqual("supported: Automatic, Full, Limited 16:235", dp4)
        edp1_expected_keys = {
            "EDID",
            "EdidModel",
            "scaling mode",
            "Colorspace",
            "max bpc",
            "Broadcast RGB",
            "panel orientation",
            "link-status",
            "CTM",
            "CONNECTOR_ID",
            "non-desktop",
        }
        actual_keys = set(actual["screens"][0]["devices"][0]["props"].keys())
        self.assertSetEqual(edp1_expected_keys, actual_keys)
        expected_edid_model = {
            "name": "Generic",
            "product_id": "22333",
            "serial_number": "0",
        }
        self.assertDictEqual(
            expected_edid_model,
            actual["screens"][0]["devices"][0]["props"]["EdidModel"],  # type: ignore
        )

    def test_issue_549(self):
        """https://github.com/kellyjonbrazil/jc/issues/549"""
        with open("tests/fixtures/generic/xrandr_extra_hv_lines.out", "r") as f:
            actual = parse(f.read(), quiet=True)

        with open('tests/fixtures/generic/xrandr_extra_hv_lines.json', 'r') as f:
            reference = json.loads(f.read())

        self.assertEqual(actual, reference)


if __name__ == "__main__":
    unittest.main()
