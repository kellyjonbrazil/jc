import os
import unittest
import json
import jc.parsers.cksum

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/cksum.out'), 'r', encoding='utf-8') as f:
        centos_7_7_cksum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sum.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/cksum.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_cksum = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/sum.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_sum = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/cksum.json'), 'r', encoding='utf-8') as f:
        centos_7_7_cksum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sum.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/cksum.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_cksum_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/sum.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_sum_json = json.loads(f.read())

    def test_cksum_nodata(self):
        """
        Test 'cksum' parser with no data
        """
        self.assertEqual(jc.parsers.cksum.parse('', quiet=True), [])

    def test_cksum_centos_7_7(self):
        """
        Test 'cksum' on Centos 7.7
        """
        self.assertEqual(jc.parsers.cksum.parse(self.centos_7_7_cksum, quiet=True), self.centos_7_7_cksum_json)

    def test_sum_centos_7_7(self):
        """
        Test 'sum' on Centos 7.7
        """
        self.assertEqual(jc.parsers.cksum.parse(self.centos_7_7_sum, quiet=True), self.centos_7_7_sum_json)

    def test_cksum_osx_10_14_6(self):
        """
        Test 'cksum' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.cksum.parse(self.osx_10_14_6_cksum, quiet=True), self.osx_10_14_6_cksum_json)

    def test_sum_osx_10_14_6(self):
        """
        Test 'sum' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.cksum.parse(self.osx_10_14_6_sum, quiet=True), self.osx_10_14_6_sum_json)


if __name__ == '__main__':
    unittest.main()
