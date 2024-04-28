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

    def test_windows_systeminfo(self):
        """
        Test a sample Windows "systeminfo" command output
        """
        for tf in MyTests.test_files:
            in_var = getattr(self, self.varName(tf))
            out_var = getattr(self, self.varName(tf) + "_json")

            self.assertEqual(jc.parsers.systeminfo.parse(in_var, quiet=True), out_var)


if __name__ == "__main__":
    unittest.main()
