import os
import json
import unittest
import jc.parsers.uname
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uname-a.out'), 'r', encoding='utf-8') as f:
        centos_7_7_uname_a = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uname.out'), 'r', encoding='utf-8') as f:
        centos_7_7_uname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/uname-a.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_uname_a = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/uname-a.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_uname_a = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/uname-a.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_uname_a = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/uname.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_uname = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/uname-a.out'), 'r', encoding='utf-8') as f:
        freebsd12_uname_a = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/uname-a2.out'), 'r', encoding='utf-8') as f:
        freebsd12_uname_a2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/uname-a.out'), 'r', encoding='utf-8') as f:
        generic_uname_a = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/uname-a-different-proc.out'), 'r', encoding='utf-8') as f:
        generic_uname_a_different_proc = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/uname-a.out'), 'r', encoding='utf-8') as f:
        debian_10_uname_a = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/uname-a.json'), 'r', encoding='utf-8') as f:
        centos_7_7_uname_a_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/uname-a.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_uname_a_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/uname-a.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_uname_a_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/uname-a.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_uname_a_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/uname-a.json'), 'r', encoding='utf-8') as f:
        freebsd12_uname_a_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/uname-a2.json'), 'r', encoding='utf-8') as f:
        freebsd12_uname_a2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/uname-a.json'), 'r', encoding='utf-8') as f:
        generic_uname_a_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/uname-a-different-proc.json'), 'r', encoding='utf-8') as f:
        generic_uname_a_different_proc_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/uname-a.json'), 'r', encoding='utf-8') as f:
        debian_10_uname_a_json = json.loads(f.read())


    def test_uname_nodata(self):
        """
        Test 'uname -a' with no data
        """
        self.assertEqual(jc.parsers.uname.parse('', quiet=True), {})

    def test_uname_no_a_osx(self):
        """
        Test 'uname' without -a option on OSX. Should generate a ParseError exception
        """
        self.assertRaises(ParseError, jc.parsers.uname.parse, self.osx_10_14_6_uname, quiet=True)

    def test_uname_no_a_centos(self):
        """
        Test 'uname' without -a option on Centos. Should generate a ParseError exception
        """
        self.assertRaises(ParseError, jc.parsers.uname.parse, self.centos_7_7_uname, quiet=True)

    def test_uname_centos_7_7(self):
        """
        Test 'uname -a' on Centos 7.7
        """
        self.assertEqual(jc.parsers.uname.parse(self.centos_7_7_uname_a, quiet=True), self.centos_7_7_uname_a_json)

    def test_uname_ubuntu_18_4(self):
        """
        Test 'uname -a' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.uname.parse(self.ubuntu_18_4_uname_a, quiet=True), self.ubuntu_18_4_uname_a_json)

    def test_uname_osx_10_11_6(self):
        """
        Test 'uname -a' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.uname.parse(self.osx_10_11_6_uname_a, quiet=True), self.osx_10_11_6_uname_a_json)

    def test_uname_osx_10_14_6(self):
        """
        Test 'uname -a' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.uname.parse(self.osx_10_14_6_uname_a, quiet=True), self.osx_10_14_6_uname_a_json)

    def test_uname_freebsd12(self):
        """
        Test 'uname -a' on freebsd12
        """
        self.assertEqual(jc.parsers.uname.parse(self.freebsd12_uname_a, quiet=True), self.freebsd12_uname_a_json)

    def test_uname2_freebsd12(self):
        """
        Test 'uname -a' on freebsd12 with longer version level string
        """
        self.assertEqual(jc.parsers.uname.parse(self.freebsd12_uname_a2, quiet=True), self.freebsd12_uname_a2_json)

    def test_uname_generic(self):
        """
        Test 'uname -a' on debian with missing hardware platform and processor
        """
        self.assertEqual(jc.parsers.uname.parse(self.generic_uname_a, quiet=True), self.generic_uname_a_json)

    def test_uname_different_proc_generic(self):
        """
        Test 'uname -a' on machine with different processor type
        """
        self.assertEqual(jc.parsers.uname.parse(self.generic_uname_a_different_proc, quiet=True), self.generic_uname_a_different_proc_json)

    def test_uname_debian_10(self):
        """
        Test 'uname -a' on debian 10 with missing hardware platform and processor
        """
        self.assertEqual(jc.parsers.uname.parse(self.debian_10_uname_a, quiet=True), self.debian_10_uname_a_json)


if __name__ == '__main__':
    unittest.main()
