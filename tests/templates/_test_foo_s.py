import os
import json
import unittest
import jc.parsers.foo_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# To create streaming output use:
# $ cat foo.out | jc --foo-s | jello -c > foo-streaming.json


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/foo.out'), 'r', encoding='utf-8') as f:
        centos_7_7_foo = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/foo-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_foo_streaming_json = json.loads(f.read())

    def test_foo_s_nodata(self):
        """
        Test 'foo' with no data
        """
        self.assertEqual(list(jc.parsers.foo_s.parse([], quiet=True)), [])

    def test_foo_s_centos_7_7(self):
        """
        Test 'foo' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.foo_s.parse(self.centos_7_7_foo.splitlines(), quiet=True)), self.centos_7_7_foo_streaming_json)


if __name__ == '__main__':
    unittest.main()
