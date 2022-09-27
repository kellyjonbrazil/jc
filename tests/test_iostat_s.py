import os
import json
import unittest
from jc.exceptions import ParseError
import jc.parsers.iostat_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat iostat.out | jc --iostat-s | jello -c > iostat-streaming.json


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-m.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_m = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-x.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_x = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-mx.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_mx = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-1.out'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-m.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_m = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-x.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_x = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-mx.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_mx = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-1.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_1 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-m.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_m = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-x.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_x = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-mx.out'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_mx = f.read()

    # output

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-m-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_m_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-x-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_x_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-mx-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_mx_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/iostat-1-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_iostat_1_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-m-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_m_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-x-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_x_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-mx-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_mx_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/iostat-1-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_iostat_1_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-m-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_m_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-x-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_x_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-20.10/iostat-mx-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_20_10_iostat_mx_streaming_json = json.loads(f.read())


    def test_iostat_empty_dir(self):
        """
        Test plain 'ls' on an empty directory
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse([], quiet=True)), [])

    def test_iostat_raise_exception(self):
        """
        Test non-iostat data (raises ParseError)
        """
        g = jc.parsers.iostat_s.parse(['not iostat data','not iostat data'], quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_iostat_centos_7_7(self):
        """
        Test 'iostat' on centos 7
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.centos_7_7_iostat.splitlines(), quiet=True)), self.centos_7_7_iostat_streaming_json)

    def test_iostat_m_centos_7_7(self):
        """
        Test 'iostat -m' on centos 7
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.centos_7_7_iostat_m.splitlines(), quiet=True)), self.centos_7_7_iostat_m_streaming_json)

    def test_iostat_x_centos_7_7(self):
        """
        Test 'iostat -x' on centos 7
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.centos_7_7_iostat_x.splitlines(), quiet=True)), self.centos_7_7_iostat_x_streaming_json)

    def test_iostat_mx_centos_7_7(self):
        """
        Test 'iostat -mx' on centos 7
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.centos_7_7_iostat_mx.splitlines(), quiet=True)), self.centos_7_7_iostat_mx_streaming_json)

    def test_iostat_1_centos_7_7(self):
        """
        Test 'iostat 1' on centos 7
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.centos_7_7_iostat_1.splitlines(), quiet=True)), self.centos_7_7_iostat_1_streaming_json)

    def test_iostat_ubuntu_18_4(self):
        """
        Test 'iostat' on ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.ubuntu_18_4_iostat.splitlines(), quiet=True)), self.ubuntu_18_4_iostat_streaming_json)

    def test_iostat_m_ubuntu_18_4(self):
        """
        Test 'iostat -m' on ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.ubuntu_18_4_iostat_m.splitlines(), quiet=True)), self.ubuntu_18_4_iostat_m_streaming_json)

    def test_iostat_x_ubuntu_18_4(self):
        """
        Test 'iostat -x' on ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.ubuntu_18_4_iostat_x.splitlines(), quiet=True)), self.ubuntu_18_4_iostat_x_streaming_json)

    def test_iostat_mx_ubuntu_18_4(self):
        """
        Test 'iostat -mx' on ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.ubuntu_18_4_iostat_mx.splitlines(), quiet=True)), self.ubuntu_18_4_iostat_mx_streaming_json)

    def test_iostat_1_ubuntu_18_4(self):
        """
        Test 'iostat 1' on ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.ubuntu_18_4_iostat_1.splitlines(), quiet=True)), self.ubuntu_18_4_iostat_1_streaming_json)

    def test_iostat_ubuntu_20_10(self):
        """
        Test 'iostat' on ubuntu 20.10
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.ubuntu_20_10_iostat.splitlines(), quiet=True)), self.ubuntu_20_10_iostat_streaming_json)

    def test_iostat_m_ubuntu_20_10(self):
        """
        Test 'iostat -m' on ubuntu 20.10
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.ubuntu_20_10_iostat_m.splitlines(), quiet=True)), self.ubuntu_20_10_iostat_m_streaming_json)

    def test_iostat_x_ubuntu_20_10(self):
        """
        Test 'iostat -x' on ubuntu 20.10
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.ubuntu_20_10_iostat_x.splitlines(), quiet=True)), self.ubuntu_20_10_iostat_x_streaming_json)

    def test_iostat_mx_ubuntu_20_10(self):
        """
        Test 'iostat -mx' on ubuntu 20.10
        """
        self.assertEqual(list(jc.parsers.iostat_s.parse(self.ubuntu_20_10_iostat_mx.splitlines(), quiet=True)), self.ubuntu_20_10_iostat_mx_streaming_json)


if __name__ == '__main__':
    unittest.main()
