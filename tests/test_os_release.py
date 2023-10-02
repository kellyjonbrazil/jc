import os
import unittest
import json
from typing import Dict
from jc.parsers.os_release import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'os_release_centos': (
                'fixtures/generic/os-release-centos',
                'fixtures/generic/os-release-centos.json'),
            'os_release_ubuntu': (
                'fixtures/generic/os-release-ubuntu',
                'fixtures/generic/os-release-ubuntu.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_os_release_nodata(self):
        """
        Test 'os_release' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_os_release_centos(self):
        """
        Test 'os_release' on Centos
        """
        self.assertEqual(
            parse(self.f_in['os_release_centos'], quiet=True),
            self.f_json['os_release_centos']
        )

    def test_os_release_ubuntu(self):
        """
        Test 'os_release' on ubuntu
        """
        self.assertEqual(
            parse(self.f_in['os_release_ubuntu'], quiet=True),
            self.f_json['os_release_ubuntu']
        )


if __name__ == '__main__':
    unittest.main()
