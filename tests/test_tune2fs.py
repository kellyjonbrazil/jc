import os
import unittest
import json
from typing import Dict
from jc.parsers.tune2fs import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'tune2fs': (
                'fixtures/generic/tune2fs-l.out',
                'fixtures/generic/tune2fs-l.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_tune2fs_line_separators(self):
        """
        Test 'tune2fs' with line-break characters other than LF in the volume name and mount point
        """
        data = 'tune2fs 1.46.2 (28-Feb-2021)\nFilesystem volume name:   va\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\nLast mounted on:          /home/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\nFilesystem UUID:          5fb78e1a-b214-44e2-a309-8e35116d8dd6\n'
        result = parse(data, quiet=True)
        self.assertEqual(result['filesystem_volume_name'], 'va\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result['last_mounted_on'], '/home/a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result['filesystem_uuid'], '5fb78e1a-b214-44e2-a309-8e35116d8dd6')

    def test_tune2fs_nodata(self):
        """
        Test 'tune2fs' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_tune2fs_l(self):
        """
        Test 'tune2fs -l'
        """
        self.assertEqual(
            parse(self.f_in['tune2fs'], quiet=True),
            self.f_json['tune2fs']
        )


if __name__ == '__main__':
    unittest.main()
