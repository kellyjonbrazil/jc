import os
import unittest
import json
from typing import Dict
from jc.parsers.pkg_index_apk import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class Apkindex(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'normal': (
                'fixtures/generic/pkg-index-apk.out',
                'fixtures/generic/pkg-index-apk.json'),
            'raw': (
                'fixtures/generic/pkg-index-apk.out',
                'fixtures/generic/pkg-index-apk-raw.json'),
            'long_maintainer': (
                'fixtures/generic/pkg-index-apk-long-maintainer.out',
                'fixtures/generic/pkg-index-apk-long-maintainer.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_pkg_index_apk_nodata(self):
        """
        Test 'pkg-index-apk' with no data
        """
        self.assertEqual(parse('', quiet=True), [])


    def test_pkg_index_apk(self):
        """
        Test 'pkg-index-apk' normal output
        """
        self.assertEqual(
            parse(self.f_in['normal'], quiet=True),
            self.f_json['normal']
        )


    def test_pkg_index_apk_raw(self):
        """
        Test 'pkg-index-apk' raw output
        """
        self.assertEqual(
            parse(self.f_in['raw'], quiet=True, raw=True),
            self.f_json['raw']
        )


    def test_pkg_index_apk_line_separator(self):
        """
        Test 'pkg_index_apk' with a line-break character other than LF inside a field
        """
        data = 'P:yasm\nT:Assembler\u2028\u2028P:openssl\nD:so:libc.musl-x86_64.so.1\n'
        result = parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['package'], 'yasm')
        self.assertEqual(result[0]['description'], 'Assembler\u2028\u2028P:openssl')


    def test_pkg_index_apk_long_maintainer(self):
        """
        Test 'pkg-index-apk' with a long maintainer value that repeats ' <'
        without a closing '>'
        """
        self.assertEqual(
            parse(self.f_in['long_maintainer'], quiet=True),
            self.f_json['long_maintainer']
        )


    def test_pkg_index_apk_maintainer_split(self):
        """
        Test 'pkg-index-apk' maintainer name and email: the email ends at the
        last '>' and starts after the last ' <' before it
        """
        cases = {
            'Natanael Copa <ncopa@alpinelinux.org>': {'name': 'Natanael Copa', 'email': 'ncopa@alpinelinux.org'},
            'Natanael Copa': {'name': 'Natanael Copa'},
            'A <b> c>': {'name': 'A', 'email': 'b> c'},
            'A <b<c>': {'name': 'A', 'email': 'b<c'},
            'A < B <c@d> x': {'name': 'A < B', 'email': 'c@d'},
            'A <b': {'name': 'A <b'},
            'A <>': {'name': 'A', 'email': ''},
            '<a@b>': {'name': '<a@b>'}
        }

        for value, expected in cases.items():
            with self.subTest(value):
                self.assertEqual(parse('P:x\nm:' + value + '\n', quiet=True)[0]['maintainer'], expected)


if __name__ == "__main__":
    unittest.main()
