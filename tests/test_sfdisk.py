import os
import json
import unittest
import jc.parsers.sfdisk

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-l.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_l = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-l-multi.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_l_multi = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-d.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_d = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-d-multi.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_d_multi = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-luB.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_luB = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-luM.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_luM = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-luS.out'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_luS = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-8/sfdisk-l.out'), 'r', encoding='utf-8') as f:
        centos_8_sfdisk_l = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-8/sfdisk-F.out'), 'r', encoding='utf-8') as f:
        centos_8_sfdisk_F = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/sfdisk-l.out'), 'r', encoding='utf-8') as f:
        debian_10_sfdisk_l = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/sfdisk-l2.out'), 'r', encoding='utf-8') as f:
        debian_10_sfdisk_l2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/sfdisk-l3.out'), 'r', encoding='utf-8') as f:
        debian_10_sfdisk_l3 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/sfdisk-F.out'), 'r', encoding='utf-8') as f:
        debian_10_sfdisk_F = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/sfdisk-F2.out'), 'r', encoding='utf-8') as f:
        debian_10_sfdisk_F2 = f.read()


    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-l.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_l_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-l-multi.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_l_multi_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-d.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_d_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-d-multi.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_d_multi_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-luB.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_luB_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-luM.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_luM_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/sfdisk-luS.json'), 'r', encoding='utf-8') as f:
        centos_7_7_sfdisk_luS_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-8/sfdisk-l.json'), 'r', encoding='utf-8') as f:
        centos_8_sfdisk_l_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-8/sfdisk-F.json'), 'r', encoding='utf-8') as f:
        centos_8_sfdisk_F_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/sfdisk-l.json'), 'r', encoding='utf-8') as f:
        debian_10_sfdisk_l_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/sfdisk-l2.json'), 'r', encoding='utf-8') as f:
        debian_10_sfdisk_l2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/sfdisk-l3.json'), 'r', encoding='utf-8') as f:
        debian_10_sfdisk_l3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/sfdisk-F.json'), 'r', encoding='utf-8') as f:
        debian_10_sfdisk_F_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian10/sfdisk-F2.json'), 'r', encoding='utf-8') as f:
        debian_10_sfdisk_F2_json = json.loads(f.read())


    def test_sfdisk_nodata(self):
        """
        Test 'sfdisk' with no data
        """
        self.assertEqual(jc.parsers.sfdisk.parse('', quiet=True), [])

    def test_sfdisk_l_centos_7_7(self):
        """
        Test 'sfdisk -l' on Centos 7.7
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.centos_7_7_sfdisk_l, quiet=True), self.centos_7_7_sfdisk_l_json)

    def test_sfdisk_l_multi_centos_7_7(self):
        """
        Test 'sfdisk -l' with multiple disk data on Centos 7.7
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.centos_7_7_sfdisk_l_multi, quiet=True), self.centos_7_7_sfdisk_l_multi_json)

    def test_sfdisk_d_centos_7_7(self):
        """
        Test 'sfdisk -d' on Centos 7.7
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.centos_7_7_sfdisk_d, quiet=True), self.centos_7_7_sfdisk_d_json)

    def test_sfdisk_d_multi_centos_7_7(self):
        """
        Test 'sfdisk -d' with multiple disk data on Centos 7.7
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.centos_7_7_sfdisk_d_multi, quiet=True), self.centos_7_7_sfdisk_d_multi_json)

    def test_sfdisk_luB_centos_7_7(self):
        """
        Test 'sfdisk -luB' on Centos 7.7
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.centos_7_7_sfdisk_luB, quiet=True), self.centos_7_7_sfdisk_luB_json)

    def test_sfdisk_luM_centos_7_7(self):
        """
        Test 'sfdisk -luM' on Centos 7.7
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.centos_7_7_sfdisk_luM, quiet=True), self.centos_7_7_sfdisk_luM_json)

    def test_sfdisk_luS_centos_7_7(self):
        """
        Test 'sfdisk -luS' on Centos 7.7
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.centos_7_7_sfdisk_luS, quiet=True), self.centos_7_7_sfdisk_luS_json)

    def test_sfdisk_l_centos_8(self):
        """
        Test 'sfdisk -l' on Centos 8
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.centos_8_sfdisk_l, quiet=True), self.centos_8_sfdisk_l_json)

    def test_sfdisk_F_centos_8(self):
        """
        Test 'sfdisk -F' on Centos 8
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.centos_8_sfdisk_F, quiet=True), self.centos_8_sfdisk_F_json)

    def test_sfdisk_l_debian_10(self):
        """
        Test 'sfdisk -l' on Debian 10
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.debian_10_sfdisk_l, quiet=True), self.debian_10_sfdisk_l_json)

    def test_sfdisk_l2_debian_10(self):
        """
        Test 'sfdisk -l' on Debian 10 (second example)
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.debian_10_sfdisk_l2, quiet=True), self.debian_10_sfdisk_l2_json)

    def test_sfdisk_l3_debian_10(self):
        """
        Test 'sfdisk -l' on Debian 10 (third example)
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.debian_10_sfdisk_l3, quiet=True), self.debian_10_sfdisk_l3_json)

    def test_sfdisk_F_debian10(self):
        """
        Test 'sfdisk -F' on Debian 10
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.debian_10_sfdisk_F, quiet=True), self.debian_10_sfdisk_F_json)

    def test_sfdisk_F2_debian10(self):
        """
        Test 'sfdisk -F' on Debian 10 (second example)
        """
        self.assertEqual(jc.parsers.sfdisk.parse(self.debian_10_sfdisk_F2, quiet=True), self.debian_10_sfdisk_F2_json)


if __name__ == '__main__':
    unittest.main()
