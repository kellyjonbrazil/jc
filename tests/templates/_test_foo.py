import os
import unittest
import json
import jc.parsers.foo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # input
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/foo.out'), 'r', encoding='utf-8') as f:
            self.centos_7_7_foo = f.read()

        # output
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/foo.json'), 'r', encoding='utf-8') as f:
            self.centos_7_7_foo_json = json.loads(f.read())


    def test_foo_nodata(self):
        """
        Test 'foo' with no data
        """
        self.assertEqual(jc.parsers.foo.parse('', quiet=True), [])

    def test_foo_centos_7_7(self):
        """
        Test 'foo' on Centos 7.7
        """
        self.assertEqual(jc.parsers.foo.parse(self.centos_7_7_foo, quiet=True), self.centos_7_7_foo_json)


if __name__ == '__main__':
    unittest.main()
