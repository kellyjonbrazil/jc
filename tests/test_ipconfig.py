import json
import os
import unittest
import jc.parsers.ipconfig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    test_files = [
        "tests/fixtures/windows/windows-xp/ipconfig",
        "tests/fixtures/windows/windows-7/ipconfig",
        "tests/fixtures/windows/windows-10/ipconfig",
        "tests/fixtures/windows/windows-11/ipconfig",
        "tests/fixtures/windows/windows-2008/ipconfig",
        "tests/fixtures/windows/windows-2016/ipconfig",
    ]

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ipconfig-long-line.out'), 'r', encoding='utf-8') as f:
        generic_ipconfig_long_line = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ipconfig-long-line.json'), 'r', encoding='utf-8') as f:
        generic_ipconfig_long_line_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ipconfig-adapter-banner-name.out'), 'r', encoding='utf-8') as f:
        generic_ipconfig_adapter_banner_name = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ipconfig-adapter-banner-name.json'), 'r', encoding='utf-8') as f:
        generic_ipconfig_adapter_banner_name_json = json.loads(f.read())

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

    def test_windows_ipconfig(self):
        """
        Test a sample Windows "ipconfig" command output
        """
        for tf in MyTests.test_files:
            in_var = getattr(self, self.varName(tf))
            out_var = getattr(self, self.varName(tf) + "_json")

            self.assertEqual(jc.parsers.ipconfig.parse(in_var, quiet=True), out_var)


    def test_ipconfig_line_separator(self):
        """
        Test 'ipconfig' with a line-break character other than LF inside a field
        """
        data = self._windows_10_ipconfig.replace('adapter Ethernet 2:', 'adapter Ethernet\u20282:')
        result = jc.parsers.ipconfig.parse(data, quiet=True)
        self.assertEqual([x['name'] for x in result['adapters']], ['Tailscale', 'Ethernet\u20282', 'Bluetooth Network Connection'])
        self.assertEqual(result['adapters'][0]['physical_address'], None)

    def test_ipconfig_long_line(self):
        """
        Test 'ipconfig' with a long line that repeats 'adapter' and has no colon
        """
        self.assertEqual(jc.parsers.ipconfig.parse(self.generic_ipconfig_long_line, quiet=True), self.generic_ipconfig_long_line_json)

    def test_ipconfig_adapter_banner_name(self):
        """
        Test 'ipconfig' with a first adapter named 'Windows IP Configuration'
        """
        self.assertEqual(jc.parsers.ipconfig.parse(self.generic_ipconfig_adapter_banner_name, quiet=True), self.generic_ipconfig_adapter_banner_name_json)


if __name__ == "__main__":
    unittest.main()
