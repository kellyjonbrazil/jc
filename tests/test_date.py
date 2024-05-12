import os
import json
import unittest
import jc.parsers.date

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/date.out'), 'r', encoding='utf-8') as f:
        generic_date = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/date-before-midnight.out'), 'r', encoding='utf-8') as f:
        generic_date_before_midnight = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/date-after-midnight.out'), 'r', encoding='utf-8') as f:
        generic_date_after_midnight = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/date.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_04_date = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/date2.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_04_date2 = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/date.json'), 'r', encoding='utf-8') as f:
        generic_date_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/date-before-midnight.json'), 'r', encoding='utf-8') as f:
        generic_date_before_midnight_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/date-after-midnight.json'), 'r', encoding='utf-8') as f:
        generic_date_after_midnight_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/date.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_04_date_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.04/date2.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_04_date2_json = json.loads(f.read())


    def test_date_nodata(self):
        """
        Test 'date' with no data
        """
        self.assertEqual(jc.parsers.date.parse('', quiet=True), {})

    def test_date(self):
        """
        Test 'date'
        """
        self.assertEqual(jc.parsers.date.parse(self.generic_date, quiet=True), self.generic_date_json)

    def test_date_before_midnight(self):
        """
        Test 'date' 24-hour conversion just before midnight
        """
        self.assertEqual(jc.parsers.date.parse(self.generic_date_before_midnight, quiet=True), self.generic_date_before_midnight_json)

    def test_date_after_midnight(self):
        """
        Test 'date' 24-hour conversion just after midnight
        """
        self.assertEqual(jc.parsers.date.parse(self.generic_date_after_midnight, quiet=True), self.generic_date_after_midnight_json)

    def test_date_am_ubuntu_20_04(self):
        """
        Test 'date' on Ubuntu 20.4 with LANG=en_US.UTF-8 (uses 12-hour clock) with AM time
        """
        self.assertEqual(jc.parsers.date.parse(self.ubuntu_20_04_date, quiet=True), self.ubuntu_20_04_date_json)

    def test_date_pm_ubuntu_20_04(self):
        """
        Test 'date' on Ubuntu 20.4 with LANG=en_US.UTF-8 (uses 12-hour clock) with PM time
        """
        self.assertEqual(jc.parsers.date.parse(self.ubuntu_20_04_date2, quiet=True), self.ubuntu_20_04_date2_json)


if __name__ == '__main__':
    unittest.main()
