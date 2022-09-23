import os
import json
import unittest
import jc.parsers.dmidecode

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dmidecode.out'), 'r', encoding='utf-8') as f:
        centos_7_7_dmidecode = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dmidecode.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dmidecode = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/dmidecode.out'), 'r', encoding='utf-8') as f:
        fedora32_dmidecode = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dmidecode.json'), 'r', encoding='utf-8') as f:
        centos_7_7_dmidecode_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dmidecode.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dmidecode_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/fedora32/dmidecode.json'), 'r', encoding='utf-8') as f:
        fedora32_dmidecode_json = json.loads(f.read())


    def test_dmidecode_nodata(self):
        """
        Test 'dmidecode' with no data
        """
        self.assertEqual(jc.parsers.dmidecode.parse('', quiet=True), [])

    def test_dmidecode_centos_7_7(self):
        """
        Test 'dmidecode' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dmidecode.parse(self.centos_7_7_dmidecode, quiet=True), self.centos_7_7_dmidecode_json)

    def test_dmidecode_ubuntu_18_4(self):
        """
        Test 'dmidecode' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dmidecode.parse(self.ubuntu_18_4_dmidecode, quiet=True), self.ubuntu_18_4_dmidecode_json)

    def test_dmidecode_fedora32(self):
        """
        Test 'dmidecode' on Fedora 32
        """
        self.assertEqual(jc.parsers.dmidecode.parse(self.fedora32_dmidecode, quiet=True), self.fedora32_dmidecode_json)


if __name__ == '__main__':
    unittest.main()
