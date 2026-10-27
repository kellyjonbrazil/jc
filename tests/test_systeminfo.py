import json
import os
import unittest
import jc.parsers.systeminfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    test_files = [
        "tests/fixtures/windows/windows-7/systeminfo",
        "tests/fixtures/windows/windows-10/systeminfo",
        "tests/fixtures/windows/windows-10/systeminfo-hyperv",
        "tests/fixtures/windows/windows-10/systeminfo-hyperv-utc",
        "tests/fixtures/windows/windows-2012r2/systeminfo",
    ]

    def setUp(self):
        for tf in MyTests.test_files:
            in_file = os.path.join(THIS_DIR, os.pardir, f"{tf}.out")
            out_file = os.path.join(THIS_DIR, os.pardir, f"{tf}.json")

            with open(in_file, "r", encoding="utf-8") as f:
                setattr(self, self.varName(tf), f.read())
            with open(out_file, "r", encoding="utf-8") as f:
                setattr(self, self.varName(tf) + "_json", json.loads(f.read()))

    def varName(self, path):
        return (
            path.replace("tests/fixtures/windows", "")
            .replace("-", "_")
            .replace("/", "_")
        )

    def test_systeminfo_truncated(self):
        """
        Test 'systeminfo' output cut short, e.g. `systeminfo | head -5 |
        jc --systeminfo`. _process() used to assume every key it converts was
        present, raising KeyError on 'network_cards' and then on the integer
        fields, and UnboundLocalError when no time zone had been parsed.
        """
        truncated = (
            'Host Name:                 WIN-ABC123\n'
            'OS Name:                   Microsoft Windows 10 Pro\n'
            'OS Version:                10.0.19042 N/A Build 19042\n'
        )
        parsed = jc.parsers.systeminfo.parse(truncated, quiet=True)
        self.assertEqual(parsed['host_name'], 'WIN-ABC123')
        self.assertEqual(parsed['os_name'], 'Microsoft Windows 10 Pro')

    def test_windows_systeminfo(self):
        """
        Test a sample Windows "systeminfo" command output
        """
        for tf in MyTests.test_files:
            in_var = getattr(self, self.varName(tf))
            out_var = getattr(self, self.varName(tf) + "_json")

            self.assertEqual(jc.parsers.systeminfo.parse(in_var, quiet=True), out_var)

    def test_systeminfo_multiline_values(self):
        """
        Test 'systeminfo' values that span several lines
        """
        data = 'Host Name:                 H\nOS Name:                   X\nHotfix(s):                 2 Hotfix(s) Installed.\n                           [01]: KB1\n                           [02]: KB2\nBIOS Version:              abc\n                           def\n'
        expected = {
            'host_name': 'H',
            'os_name': 'X',
            'hotfixs': ['KB1', 'KB2'],
            'bios_version': 'abc\n                           def'
        }
        self.assertEqual(jc.parsers.systeminfo.parse(data, raw=True, quiet=True), expected)


if __name__ == "__main__":
    unittest.main()
