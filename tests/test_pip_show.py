import os
import json
import unittest
import jc.parsers.pip_show

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pip-show.out'), 'r', encoding='utf-8') as f:
        centos_7_7_pip_show = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/pip-show.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_pip_show = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/pip-show.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_pip_show = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/pip-show.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_pip_show = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pip-show-multiline-license.out'), 'r', encoding='utf-8') as f:
        generic_pip_show_multiline_license = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pip-show-multiline-license-first-blank.out'), 'r', encoding='utf-8') as f:
        generic_pip_show_multiline_license_first_blank = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/pip-show.json'), 'r', encoding='utf-8') as f:
        centos_7_7_pip_show_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/pip-show.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_pip_show_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/pip-show.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_pip_show_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/pip-show.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_pip_show_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pip-show-multiline-license.json'), 'r', encoding='utf-8') as f:
        generic_pip_show_multiline_license_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/pip-show-multiline-license-first-blank.json'), 'r', encoding='utf-8') as f:
        generic_pip_show_multiline_license_first_blank_json = json.loads(f.read())


    def test_pip_show_nodata(self):
        """
        Test 'pip show' with no data
        """
        self.assertEqual(jc.parsers.pip_show.parse('', quiet=True), [])

    def test_pip_show_centos_7_7(self):
        """
        Test 'pip show' on Centos 7.7
        """
        self.assertEqual(jc.parsers.pip_show.parse(self.centos_7_7_pip_show, quiet=True), self.centos_7_7_pip_show_json)

    def test_pip_show_ubuntu_18_4(self):
        """
        Test 'pip show' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.pip_show.parse(self.ubuntu_18_4_pip_show, quiet=True), self.ubuntu_18_4_pip_show_json)

    def test_pip_show_osx_10_11_6(self):
        """
        Test 'pip show' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.pip_show.parse(self.osx_10_11_6_pip_show, quiet=True), self.osx_10_11_6_pip_show_json)

    def test_pip_show_osx_10_14_6(self):
        """
        Test 'pip show' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.pip_show.parse(self.osx_10_14_6_pip_show, quiet=True), self.osx_10_14_6_pip_show_json)

    def test_pip_show_multiline_license(self):
        """
        Test 'pip show' with a multiline license
        """
        self.assertEqual(jc.parsers.pip_show.parse(self.generic_pip_show_multiline_license, quiet=True), self.generic_pip_show_multiline_license_json)

    def test_pip_show_multiline_license_first_blank(self):
        """
        Test 'pip show' with a multiline license where the first line is blank
        """
        self.assertEqual(jc.parsers.pip_show.parse(self.generic_pip_show_multiline_license_first_blank, quiet=True), self.generic_pip_show_multiline_license_first_blank_json)

    def test_pip_show_files_section(self):
        """
        Test 'pip show -f' output with a files section
        """
        data = """\
Name: jc
Version: 1.25.4
Summary: Converts the output of popular command-line tools and file-types to JSON.
Home-page: https://github.com/kellyjonbrazil/jc
Author: Kelly Brazil
Author-email: kelly@gmail.com
License: MIT
Location: /home/pi/.local/lib/python3.11/site-packages
Requires: Pygments, ruamel.yaml, xmltodict
Required-by: pypiwifi
Files:
  ../../../bin/jc
  jc-1.25.4.dist-info/RECORD
"""
        expected = [{
            'name': 'jc',
            'version': '1.25.4',
            'summary': 'Converts the output of popular command-line tools and file-types to JSON.',
            'home_page': 'https://github.com/kellyjonbrazil/jc',
            'author': 'Kelly Brazil',
            'author_email': 'kelly@gmail.com',
            'license': 'MIT',
            'location': '/home/pi/.local/lib/python3.11/site-packages',
            'requires': 'Pygments, ruamel.yaml, xmltodict',
            'required_by': 'pypiwifi',
            'files': ['../../../bin/jc', 'jc-1.25.4.dist-info/RECORD']
        }]
        self.assertEqual(jc.parsers.pip_show.parse(data, quiet=True), expected)

    def test_pip_show_files_section_with_following_field(self):
        """
        Test 'pip show -f' output when the files section is followed by a new field
        """
        data = """\
Name: jc
Files:
  ../../../bin/jc
  jc-1.25.4.dist-info/RECORD
Foo: bar
"""
        expected = [{
            'name': 'jc',
            'files': ['../../../bin/jc', 'jc-1.25.4.dist-info/RECORD'],
            'foo': 'bar'
        }]
        self.assertEqual(jc.parsers.pip_show.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
