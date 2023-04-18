import os
import unittest
import json
import jc.parsers.acpi

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-V.out'), 'r', encoding='utf-8') as f:
        generic_acpi_V = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-V2.out'), 'r', encoding='utf-8') as f:
        generic_acpi_V2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-V3.out'), 'r', encoding='utf-8') as f:
        generic_acpi_V3 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-V4.out'), 'r', encoding='utf-8') as f:
        generic_acpi_V4 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/acpi-V.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_acpi_V = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-V-never-fully-discharge.out'), 'r', encoding='utf-8') as f:
        acpi_V_never_fully_discharge = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-not-charging.out'), 'r', encoding='utf-8') as f:
        acpi_not_charging = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-V.json'), 'r', encoding='utf-8') as f:
        generic_acpi_V_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-V2.json'), 'r', encoding='utf-8') as f:
        generic_acpi_V2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-V3.json'), 'r', encoding='utf-8') as f:
        generic_acpi_V3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-V4.json'), 'r', encoding='utf-8') as f:
        generic_acpi_V4_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/acpi-V.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_acpi_V_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-V-never-fully-discharge.json'), 'r', encoding='utf-8') as f:
        acpi_V_never_fully_discharge_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/acpi-not-charging.json'), 'r', encoding='utf-8') as f:
        acpi_not_charging_json = json.loads(f.read())

    def test_acpi_nodata(self):
        """
        Test 'acpi' with no data
        """
        self.assertEqual(jc.parsers.acpi.parse('', quiet=True), [])

    def test_acpi_V_all(self):
        """
        Test 'acpi -V' with all known options
        """
        self.assertEqual(jc.parsers.acpi.parse(self.generic_acpi_V, quiet=True), self.generic_acpi_V_json)

    def test_acpi_V2(self):
        """
        Test 'acpi -V' from internet sample
        """
        self.assertEqual(jc.parsers.acpi.parse(self.generic_acpi_V2, quiet=True), self.generic_acpi_V2_json)

    def test_acpi_V3(self):
        """
        Test 'acpi -V' from internet sample
        """
        self.assertEqual(jc.parsers.acpi.parse(self.generic_acpi_V3, quiet=True), self.generic_acpi_V3_json)

    def test_acpi_V4(self):
        """
        Test 'acpi -V' from internet sample
        """
        self.assertEqual(jc.parsers.acpi.parse(self.generic_acpi_V4, quiet=True), self.generic_acpi_V4_json)

    def test_acpi_V_ubuntu(self):
        """
        Test 'acpi -V' on Ubuntu 18.04
        """
        self.assertEqual(jc.parsers.acpi.parse(self.ubuntu_18_04_acpi_V, quiet=True), self.ubuntu_18_04_acpi_V_json)

    def test_acpi_V_never_fully_discharge(self):
        """
        Test 'acpi -V' with "never fully discharge" message
        """
        self.assertEqual(jc.parsers.acpi.parse(self.acpi_V_never_fully_discharge, quiet=True), self.acpi_V_never_fully_discharge_json)

    def test_acpi_not_charging(self):
        """
        Test 'acpi' with "Not charging" message
        """
        self.assertEqual(jc.parsers.acpi.parse(self.acpi_not_charging, quiet=True), self.acpi_not_charging_json)


if __name__ == '__main__':
    unittest.main()
