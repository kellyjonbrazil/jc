import json
import os
import unittest
import jc.parsers.systeminfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    def setUp(self):
        # input
        with open(
            os.path.join(
                THIS_DIR, os.pardir, "tests/fixtures/windows/windows-10/systeminfo.out"
            ),
            "r",
            encoding="utf-8",
        ) as f:
            self.windows_10_systeminfo = f.read()

        with open(
            os.path.join(
                THIS_DIR, os.pardir, "tests/fixtures/windows/windows-7/systeminfo.out"
            ),
            "r",
            encoding="utf-8",
        ) as f:
            self.windows_7_systeminfo = f.read()

        # output
        with open(
            os.path.join(
                THIS_DIR, os.pardir, "tests/fixtures/windows/windows-10/systeminfo.json"
            ),
            "r",
            encoding="utf-8",
        ) as f:
            self.windows_10_systeminfo_json = json.loads(f.read())

        with open(
            os.path.join(
                THIS_DIR, os.pardir, "tests/fixtures/windows/windows-7/systeminfo.json"
            ),
            "r",
            encoding="utf-8",
        ) as f:
            self.windows_7_systeminfo_json = json.loads(f.read())

    def test_windows_systeminfo(self):
        """
        Test a sample Windows "systeminfo" command output
        """
        self.assertEqual(
            jc.parsers.systeminfo.parse(self.windows_10_systeminfo, quiet=True),
            self.windows_10_systeminfo_json,
        )

        self.assertEqual(
            jc.parsers.systeminfo.parse(self.windows_7_systeminfo, quiet=True),
            self.windows_7_systeminfo_json,
        )


if __name__ == "__main__":
    unittest.main()
