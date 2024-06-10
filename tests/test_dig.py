import os
import json
import unittest
import jc.parsers.dig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig.out'), 'r', encoding='utf-8') as f:
        centos_7_7_dig = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dig = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-x.out'), 'r', encoding='utf-8') as f:
        centos_7_7_dig_x = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-x.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dig_x = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-aaaa.out'), 'r', encoding='utf-8') as f:
        centos_7_7_dig_aaaa = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-aaaa.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dig_aaaa = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-axfr.out'), 'r', encoding='utf-8') as f:
        centos_7_7_dig_axfr = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-axfr.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dig_axfr = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_dig = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig-x.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_dig_x = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig-aaaa.out'), 'r', encoding='utf-8') as f:
        osx_10_11_6_dig_aaaa = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_dig = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-x.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_dig_x = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-aaaa.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_dig_aaaa = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-axfr.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_dig_axfr = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-noall-answer.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_dig_noall_answer = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-answer-spaces.out'), 'r', encoding='utf-8') as f:
        generic_dig_answer_spaces = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-additional.out'), 'r', encoding='utf-8') as f:
        generic_dig_additional = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-additional2.out'), 'r', encoding='utf-8') as f:
        generic_dig_additional2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-additional3.out'), 'r', encoding='utf-8') as f:
        generic_dig_additional3 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-edns.out'), 'r', encoding='utf-8') as f:
        generic_dig_edns = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-edns2.out'), 'r', encoding='utf-8') as f:
        generic_dig_edns2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-edns3.out'), 'r', encoding='utf-8') as f:
        generic_dig_edns3 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-nsid.out'), 'r', encoding='utf-8') as f:
        generic_dig_nsid = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig.json'), 'r', encoding='utf-8') as f:
        centos_7_7_dig_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dig_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-x.json'), 'r', encoding='utf-8') as f:
        centos_7_7_dig_x_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-x.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dig_x_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-aaaa.json'), 'r', encoding='utf-8') as f:
        centos_7_7_dig_aaaa_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-aaaa.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dig_aaaa_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-axfr.json'), 'r', encoding='utf-8') as f:
        centos_7_7_dig_axfr_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-axfr.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_dig_axfr_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_dig_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig-x.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_dig_x_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.11.6/dig-aaaa.json'), 'r', encoding='utf-8') as f:
        osx_10_11_6_dig_aaaa_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_dig_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-x.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_dig_x_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-aaaa.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_dig_aaaa_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-axfr.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_dig_axfr_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/dig-noall-answer.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_dig_noall_answer_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-answer-spaces.json'), 'r', encoding='utf-8') as f:
        generic_dig_answer_spaces_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-additional.json'), 'r', encoding='utf-8') as f:
        generic_dig_additional_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-additional2.json'), 'r', encoding='utf-8') as f:
        generic_dig_additional2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-additional3.json'), 'r', encoding='utf-8') as f:
        generic_dig_additional3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-edns.json'), 'r', encoding='utf-8') as f:
        generic_dig_edns_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-edns2.json'), 'r', encoding='utf-8') as f:
        generic_dig_edns2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-edns3.json'), 'r', encoding='utf-8') as f:
        generic_dig_edns3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/dig-nsid.json'), 'r', encoding='utf-8') as f:
        generic_dig_nsid_json = json.loads(f.read())


    def test_dig_nodata(self):
        """
        Test 'dig' with no data
        """
        self.assertEqual(jc.parsers.dig.parse('', quiet=True), [])

    def test_dig_centos_7_7(self):
        """
        Test 'dig' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig, quiet=True), self.centos_7_7_dig_json)

    def test_dig_ubuntu_18_4(self):
        """
        Test 'dig' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig, quiet=True), self.ubuntu_18_4_dig_json)

    def test_dig_x_centos_7_7(self):
        """
        Test 'dig -x' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig_x, quiet=True), self.centos_7_7_dig_x_json)

    def test_dig_x_ubuntu_18_4(self):
        """
        Test 'dig -x' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig_x, quiet=True), self.ubuntu_18_4_dig_x_json)

    def test_dig_aaaa_centos_7_7(self):
        """
        Test 'dig AAAA' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig_aaaa, quiet=True), self.centos_7_7_dig_aaaa_json)

    def test_dig_aaaa_ubuntu_18_4(self):
        """
        Test 'dig AAAA' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig_aaaa, quiet=True), self.ubuntu_18_4_dig_aaaa_json)

    def test_dig_axfr_centos_7_7(self):
        """
        Test 'dig axfr' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig_axfr, quiet=True), self.centos_7_7_dig_axfr_json)

    def test_dig_axfr_ubuntu_18_4(self):
        """
        Test 'dig axfr' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig_axfr, quiet=True), self.ubuntu_18_4_dig_axfr_json)

    def test_dig_osx_10_11_6(self):
        """
        Test 'dig' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_11_6_dig, quiet=True), self.osx_10_11_6_dig_json)

    def test_dig_x_osx_10_11_6(self):
        """
        Test 'dig -x' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_11_6_dig_x, quiet=True), self.osx_10_11_6_dig_x_json)

    def test_dig_aaaa_osx_10_11_6(self):
        """
        Test 'dig -aaaa' on OSX 10.11.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_11_6_dig_aaaa, quiet=True), self.osx_10_11_6_dig_aaaa_json)

    def test_dig_osx_10_14_6(self):
        """
        Test 'dig' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_14_6_dig, quiet=True), self.osx_10_14_6_dig_json)

    def test_dig_x_osx_10_14_6(self):
        """
        Test 'dig -x' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_14_6_dig_x, quiet=True), self.osx_10_14_6_dig_x_json)

    def test_dig_aaaa_osx_10_14_6(self):
        """
        Test 'dig -aaaa' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_14_6_dig_aaaa, quiet=True), self.osx_10_14_6_dig_aaaa_json)

    def test_dig_axfr_osx_10_14_6(self):
        """
        Test 'dig axfr' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_14_6_dig_axfr, quiet=True), self.osx_10_14_6_dig_axfr_json)

    def test_dig_noall_answer_osx_10_14_6(self):
        """
        Test 'dig +noall +answer' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.dig.parse(self.osx_10_14_6_dig_noall_answer, quiet=True), self.osx_10_14_6_dig_noall_answer_json)

    def test_dig_answer_spaces(self):
        """
        Test 'dig' with spaces in the answer data (e.g. TXT responses)
        """
        self.assertEqual(jc.parsers.dig.parse(self.generic_dig_answer_spaces, quiet=True), self.generic_dig_answer_spaces_json)

    def test_dig_additional(self):
        """
        Test 'dig' with additional section
        """
        self.assertEqual(jc.parsers.dig.parse(self.generic_dig_additional, quiet=True), self.generic_dig_additional_json)

    def test_dig_additional2(self):
        """
        Test 'dig' with additional section
        """
        self.assertEqual(jc.parsers.dig.parse(self.generic_dig_additional2, quiet=True), self.generic_dig_additional2_json)

    def test_dig_additional3(self):
        """
        Test 'dig' with additional section
        """
        self.assertEqual(jc.parsers.dig.parse(self.generic_dig_additional3, quiet=True), self.generic_dig_additional3_json)

    def test_dig_edns(self):
        """
        Test 'dig' with edns info
        """
        self.assertEqual(jc.parsers.dig.parse(self.generic_dig_edns, quiet=True), self.generic_dig_edns_json)

    def test_dig_edns2(self):
        """
        Test 'dig' with edns info
        """
        self.assertEqual(jc.parsers.dig.parse(self.generic_dig_edns2, quiet=True), self.generic_dig_edns2_json)

    def test_dig_edns3(self):
        """
        Test 'dig' with edns info
        """
        self.assertEqual(jc.parsers.dig.parse(self.generic_dig_edns3, quiet=True), self.generic_dig_edns3_json)

    def test_dig_nsid(self):
        """
        Test 'dig' with nsid info
        """
        self.assertEqual(jc.parsers.dig.parse(self.generic_dig_nsid, quiet=True), self.generic_dig_nsid_json)


if __name__ == '__main__':
    unittest.main()
