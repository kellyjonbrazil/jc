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


if __name__ == "__main__":
    unittest.main()
