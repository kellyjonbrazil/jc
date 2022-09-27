import os
import json
import unittest
import jc.parsers.lsusb
from jc.exceptions import ParseError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsusb.out'), 'r', encoding='utf-8') as f:
        centos_7_7_lsusb = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsusb-v.out'), 'r', encoding='utf-8') as f:
        centos_7_7_lsusb_v = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsusb-v-single.out'), 'r', encoding='utf-8') as f:
        centos_7_7_lsusb_v_single = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsusb-test-attributes.out'), 'r', encoding='utf-8') as f:
        generic_lsusb_test_attributes = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsusb-test-attributes2.out'), 'r', encoding='utf-8') as f:
        generic_lsusb_test_attributes2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsusb-t.out'), 'r', encoding='utf-8') as f:
        generic_lsusb_t = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsusb-device-qualifier.out'), 'r', encoding='utf-8') as f:
        generic_lsusb_device_qualifier = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsusb-binary-object-store.out'), 'r', encoding='utf-8') as f:
        generic_lsusb_binary_object_store = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsusb.json'), 'r', encoding='utf-8') as f:
        centos_7_7_lsusb_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsusb-v.json'), 'r', encoding='utf-8') as f:
        centos_7_7_lsusb_v_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/lsusb-v-single.json'), 'r', encoding='utf-8') as f:
        centos_7_7_lsusb_v_single_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsusb-test-attributes.json'), 'r', encoding='utf-8') as f:
        generic_lsusb_test_attributes_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsusb-test-attributes2.json'), 'r', encoding='utf-8') as f:
        generic_lsusb_test_attributes2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsusb-device-qualifier.json'), 'r', encoding='utf-8') as f:
        generic_lsusb_devicez_qualifier_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/lsusb-binary-object-store.json'), 'r', encoding='utf-8') as f:
        generic_lsusb_binary_object_store_json = json.loads(f.read())


    def test_lsusb_nodata(self):
        """
        Test 'lsusb' with no data
        """
        self.assertEqual(jc.parsers.lsusb.parse('', quiet=True), [])

    def test_lsusb_parse_error_generic(self):
        """
        Test 'lsusb' with -t option (should raise ParseError)
        """
        self.assertRaises(ParseError, jc.parsers.lsusb.parse, self.generic_lsusb_t, quiet=True)

    def test_lsusb_centos_7_7(self):
        """
        Test 'lsusb' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsusb.parse(self.centos_7_7_lsusb, quiet=True), self.centos_7_7_lsusb_json)

    def test_lsusb_v_centos_7_7(self):
        """
        Test 'lsusb -v' on Centos 7.7
        """
        self.assertEqual(jc.parsers.lsusb.parse(self.centos_7_7_lsusb_v, quiet=True), self.centos_7_7_lsusb_v_json)

    def test_lsusb_v_single_centos_7_7(self):
        """
        Test 'lsusb -v' with different hardware
        """
        self.assertEqual(jc.parsers.lsusb.parse(self.centos_7_7_lsusb_v_single, quiet=True), self.centos_7_7_lsusb_v_single_json)

    def test_lsusb_test_attributes_generic(self):
        """
        Test 'lsusb -v' with stress test attributes
        """
        self.assertEqual(jc.parsers.lsusb.parse(self.generic_lsusb_test_attributes, quiet=True), self.generic_lsusb_test_attributes_json)

    def test_lsusb_test_attributes2_generic(self):
        """
        Test 'lsusb -v' with stress test attributes 2
        """
        self.assertEqual(jc.parsers.lsusb.parse(self.generic_lsusb_test_attributes2, quiet=True), self.generic_lsusb_test_attributes2_json)

    def test_lsusb_device_qualifier(self):
        """
        Test 'lsusb -v' with device qualifier section
        """
        self.assertEqual(jc.parsers.lsusb.parse(self.generic_lsusb_device_qualifier, quiet=True), self.generic_lsusb_devicez_qualifier_json)

    def test_lsusb_binary_object_store(self):
        """
        Test 'lsusb -v' with binary object store section
        """
        self.assertEqual(jc.parsers.lsusb.parse(self.generic_lsusb_binary_object_store, quiet=True), self.generic_lsusb_binary_object_store_json)


if __name__ == '__main__':
    unittest.main()
