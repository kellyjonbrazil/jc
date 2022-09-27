import os
import unittest
import json
import jc.parsers.m3u

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/m3u-example.m3u'), 'r', encoding='utf-8') as f:
        m3u_example = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/m3u-dirty.m3u'), 'r', encoding='utf-8') as f:
        m3u_dirty = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/m3u-example.json'), 'r', encoding='utf-8') as f:
        m3u_example_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/m3u-dirty.json'), 'r', encoding='utf-8') as f:
        m3u_dirty_json = json.loads(f.read())


    def test_m3u_nodata(self):
        """
        Test 'm3u' parser with no data
        """
        self.assertEqual(jc.parsers.m3u.parse('', quiet=True), [])

    def test_m3u_example(self):
        """
        Test 'm3u' example file
        """
        self.assertEqual(jc.parsers.m3u.parse(self.m3u_example, quiet=True), self.m3u_example_json)

    def test_m3u_dirty(self):
        """
        Test 'm3u' example file with lots of difficult parsing
        """
        self.assertEqual(jc.parsers.m3u.parse(self.m3u_dirty, quiet=True), self.m3u_dirty_json)


if __name__ == '__main__':
    unittest.main()
