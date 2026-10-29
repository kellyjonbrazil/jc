import os
import unittest
import json
from typing import Dict
from jc.parsers.git_ls_remote import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'git_ls_remote': (
                'fixtures/generic/git-ls-remote.out',
                'fixtures/generic/git-ls-remote.json'),
            'git_ls_remote_raw': (
                'fixtures/generic/git-ls-remote.out',
                'fixtures/generic/git-ls-remote-raw.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_git_ls_remote_nodata(self):
        """
        Test 'git_ls_remote' with no data
        """
        self.assertEqual(parse('', quiet=True), {})

    def test_git_ls_remote(self):
        """
        Test 'git_ls_remote'
        """
        self.assertEqual(parse(
            self.f_in['git_ls_remote'], quiet=True),
            self.f_json['git_ls_remote']
        )

    def test_git_ls_remote_raw(self):
        """
        Test 'git_ls_remote' with raw option
        """
        self.assertEqual(parse(
            self.f_in['git_ls_remote_raw'], quiet=True, raw=True),
            self.f_json['git_ls_remote_raw']
        )

    def test_git_ls_remote_unicode_separators_in_ref(self):
        """
        Test 'git_ls_remote' with U+0085, U+2028, U+2029 and NBSP in ref names
        """
        data = (
            '214cd6b9e09603b3c4fa02203b24fb2bc3d4e338\trefs/heads/a\x85b\n'
            'b884f6aacca39e05994596d8fdfa7e7c4f1e0389\trefs/heads/c\u2028d\u2029e\n'
            'e416c77bed1267254da972b0f95b7ff1d43fccef\trefs/tags/f\xa0g\n'
        )
        expected = [
            {'reference': 'refs/heads/a\x85b', 'commit': '214cd6b9e09603b3c4fa02203b24fb2bc3d4e338'},
            {'reference': 'refs/heads/c\u2028d\u2029e', 'commit': 'b884f6aacca39e05994596d8fdfa7e7c4f1e0389'},
            {'reference': 'refs/tags/f\xa0g', 'commit': 'e416c77bed1267254da972b0f95b7ff1d43fccef'}
        ]
        self.assertEqual(parse(data, quiet=True, raw=True), expected)
        self.assertEqual(parse(data, quiet=True), {
            'refs/heads/a\x85b': '214cd6b9e09603b3c4fa02203b24fb2bc3d4e338',
            'refs/heads/c\u2028d\u2029e': 'b884f6aacca39e05994596d8fdfa7e7c4f1e0389',
            'refs/tags/f\xa0g': 'e416c77bed1267254da972b0f95b7ff1d43fccef'
        })

    def test_git_ls_remote_space_separated(self):
        """
        Test 'git_ls_remote' with a space instead of a tab between hash and ref
        """
        data = '214cd6b9e09603b3c4fa02203b24fb2bc3d4e338   refs/heads/dev\n'
        self.assertEqual(parse(data, quiet=True), {'refs/heads/dev': '214cd6b9e09603b3c4fa02203b24fb2bc3d4e338'})


if __name__ == '__main__':
    unittest.main()
