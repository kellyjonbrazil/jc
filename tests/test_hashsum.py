import os
import unittest
import json
import jc.parsers.hashsum

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/md5sum.out'), 'r', encoding='utf-8') as f:
        centos_7_7_md5sum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sha256sum.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sha256sum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sha384sum.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sha384sum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/md5.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_md5 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/shasum.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_shasum = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/md5sum.json'), 'r', encoding='utf-8') as f:
        centos_7_7_md5sum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sha256sum.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sha256sum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sha384sum.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sha384sum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/md5.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_md5_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/shasum.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_shasum_json = json.loads(f.read())


    def test_hashsum_nodata(self):
        """
        Test 'hashsum' parser with no data
        """
        self.assertEqual(jc.parsers.hashsum.parse('', quiet=True), [])

    def test_md5sum_centos_7_7(self):
        """
        Test 'md5sum' on Centos 7.7
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.centos_7_7_md5sum, quiet=True), self.centos_7_7_md5sum_json)

    def test_sha256sum_centos_7_7(self):
        """
        Test 'sha256sum' on Centos 7.7
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.centos_7_7_sha256sum, quiet=True), self.centos_7_7_sha256sum_json)

    def test_sha384sum_centos_7_7(self):
        """
        Test 'sha384sum' on Centos 7.7
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.centos_7_7_sha384sum, quiet=True), self.centos_7_7_sha384sum_json)

    def test_md5_osx_10_14_6(self):
        """
        Test 'md5' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.osx_10_14_6_md5, quiet=True), self.osx_10_14_6_md5_json)

    def test_shasum_osx_10_14_6(self):
        """
        Test 'shasum' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.hashsum.parse(self.osx_10_14_6_shasum, quiet=True), self.osx_10_14_6_shasum_json)


if __name__ == '__main__':
    unittest.main()
