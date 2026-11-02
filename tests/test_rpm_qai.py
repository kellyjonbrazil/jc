import os
import unittest
import json
import jc.parsers.rpm_qi

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rpm-qai.out'), 'r', encoding='utf-8') as f:
        centos_7_7_rpm_qai = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rpm-qi-package.out'), 'r', encoding='utf-8') as f:
        centos_7_7_rpm_qi_package = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rpm-qi-description-header-lines.out'), 'r', encoding='utf-8') as f:
        rpm_qi_description_header_lines = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rpm-qai.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rpm_qai_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/rpm-qi-package.json'), 'r', encoding='utf-8') as f:
        centos_7_7_rpm_qi_package_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/rpm-qi-description-header-lines.json'), 'r', encoding='utf-8') as f:
        rpm_qi_description_header_lines_json = json.loads(f.read())

    def test_rpm_qi_nodata(self):
        """
        Test 'rpm -qi' with no data
        """
        self.assertEqual(jc.parsers.rpm_qi.parse('', quiet=True), [])

    def test_rpm_qai_centos_7_7(self):
        """
        Test 'rpm -qai' on Centos 7.7
        """
        self.assertEqual(jc.parsers.rpm_qi.parse(self.centos_7_7_rpm_qai, quiet=True), self.centos_7_7_rpm_qai_json)

    def test_rpm_qi_package_centos_7_7(self):
        """
        Test 'rpm -qi make' on Centos 7.7
        """
        self.assertEqual(jc.parsers.rpm_qi.parse(self.centos_7_7_rpm_qi_package, quiet=True), self.centos_7_7_rpm_qi_package_json)

    def test_rpm_qi_description_header_lines(self):
        """
        Test 'rpm -qi' with description lines that look like record headers
        """
        self.assertEqual(jc.parsers.rpm_qi.parse(self.rpm_qi_description_header_lines, quiet=True), self.rpm_qi_description_header_lines_json)

    def test_rpm_qi_normalized_name_collision(self):
        """
        Test 'rpm -qi' where a later field name normalizes to an earlier key
        """
        data = 'Name        : foo\nVersion     : 1.0\nVersion_    : 9.9\nRelease     : 1\n'
        self.assertEqual(jc.parsers.rpm_qi.parse(data, quiet=True), [{'name': 'foo', 'version': '1.0', 'release': '1'}])


if __name__ == '__main__':
    unittest.main()
