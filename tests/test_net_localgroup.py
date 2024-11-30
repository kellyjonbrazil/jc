import json
import os
import unittest
import jc.parsers.ipconfig
import jc.parsers.net_localgroup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    test_files = [
        "tests/fixtures/windows/windows-xp/net_localgroup",
        "tests/fixtures/windows/windows-xp/net_localgroup.administrators",
        "tests/fixtures/windows/windows-7/net_localgroup",
        "tests/fixtures/windows/windows-7/net_localgroup.administrators",
        "tests/fixtures/windows/windows-2008/net_localgroup",
        "tests/fixtures/windows/windows-2008/net_localgroup.administrators",
        "tests/fixtures/windows/windows-2016/net_localgroup",
        "tests/fixtures/windows/windows-2016/net_localgroup.administrators",
        "tests/fixtures/windows/windows-10/net_localgroup",
        "tests/fixtures/windows/windows-10/net_localgroup.administrators",
        "tests/fixtures/windows/windows-11/net_localgroup",
        "tests/fixtures/windows/windows-11/net_localgroup.administrators"
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

    def test_windows_net_localgroup(self):
        """
        Test a sample Windows "net localgroup" command output
        """
        for tf in MyTests.test_files:
            in_var = getattr(self, self.varName(tf))
            out_var = getattr(self, self.varName(tf) + "_json")

            self.assertEqual(jc.parsers.net_localgroup.parse(in_var, quiet=True), out_var)


if __name__ == "__main__":
    unittest.main()
