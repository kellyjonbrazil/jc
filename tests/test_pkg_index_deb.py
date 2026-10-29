import os
import unittest
import json
from typing import Dict
from jc.parsers.pkg_index_deb import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'deb_packages_index': (
                'fixtures/generic/pkg-index-deb.out',
                'fixtures/generic/pkg-index-deb.json'),
            'deb_description_en': (
                'fixtures/generic/pkg-index-deb--description-en.out',
                'fixtures/generic/pkg-index-deb--description-en.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_pkg_index_deb_nodata(self):
        """
        Test 'pkg-index-deb' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_pkg_index_deb(self):
        """
        Test 'pkg-index-deb'
        """
        self.assertEqual(
            parse(self.f_in['deb_packages_index'], quiet=True),
            self.f_json['deb_packages_index']
        )


    def test_pkg_index_deb_description_en(self):
        """
        Test 'pkg-index-deb' where a Description-en is not inherited by
        the following packages
        """
        self.assertEqual(
            parse(self.f_in['deb_description_en'], quiet=True),
            self.f_json['deb_description_en']
        )

    def test_pkg_index_deb_line_separator(self):
        """
        Test 'pkg_index_deb' with a line-break character other than LF inside a field
        """
        data = 'Package: coolprompt\nVersion: 1.0\nDescription: A theme\u2028Package: openssl\u2028Version: 3.0.15\n\nPackage: plainpkg\nVersion: 2.0\n'
        result = parse(data, quiet=True)
        self.assertEqual([x['package'] for x in result], ['coolprompt', 'plainpkg'])
        self.assertEqual(result[0]['description'], 'A theme\u2028Package: openssl\u2028Version: 3.0.15')

    def test_pkg_index_deb_indented_continuation_lines(self):
        """
        Test 'pkg-index-deb' where indented continuation lines look like fields
        """
        data = ('Package: coolprompt\nVersion: 1.0\nSHA256: aaaa\n'
                'Description: A theme\n Package: other\n SHA256: bbbb\n Note: text\n\n'
                'Package: plainpkg\nVersion: 2.0\n')
        result = parse(data, quiet=True)
        self.assertEqual([x['package'] for x in result], ['coolprompt', 'plainpkg'])
        self.assertEqual(result[0]['sha256'], 'aaaa')
        self.assertNotIn('note', result[0])

    def test_pkg_index_deb_normalized_name_collision(self):
        """
        Test 'pkg-index-deb' where a later field name normalizes to an earlier key
        """
        data = 'Package: foo\nVersion: 1.0\nVersion_: 9.9\nVersion-: 8.8\nArchitecture: all\n'
        result = parse(data, quiet=True)
        self.assertEqual(result, [{'package': 'foo', 'version': '1.0', 'architecture': 'all'}])


if __name__ == '__main__':
    unittest.main()
