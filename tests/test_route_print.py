import json
import os
import unittest
import jc.parsers.ipconfig
import jc.parsers.net_localgroup
import jc.parsers.route_print

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    test_files = [
        "tests/fixtures/windows/windows-xp/route_print",
        "tests/fixtures/windows/windows-7/route_print",
        "tests/fixtures/windows/windows-2008/route_print",
        "tests/fixtures/windows/windows-2016/route_print",
        "tests/fixtures/windows/windows-10/route_print",
        "tests/fixtures/windows/windows-11/route_print"
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

    def test_windows_route_print(self):
        """
        Test a sample Windows "route print" command output
        """
        for tf in MyTests.test_files:
            in_var = getattr(self, self.varName(tf))
            out_var = getattr(self, self.varName(tf) + "_json")

            self.assertEqual(jc.parsers.route_print.parse(in_var, quiet=True), out_var)


if __name__ == "__main__":
    unittest.main()
