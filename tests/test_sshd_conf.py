import os
import unittest
import json
from typing import Dict
import jc.parsers.sshd_conf

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'sshd_t': (
                'fixtures/generic/sshd-T.out',
                'fixtures/generic/sshd-T.json'),
            'sshd_t_2': (
                'fixtures/generic/sshd-T-2.out',
                'fixtures/generic/sshd-T-2.json'),
            'sshd_config': (
                'fixtures/generic/sshd_config',
                'fixtures/generic/sshd_config.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_sshd_conf_nodata(self):
        """
        Test 'sshd_conf' with no data
        """
        self.assertEqual(jc.parsers.sshd_conf.parse('', quiet=True), {})

    def test_sshd_T(self):
        """
        Test 'sshd -T'
        """
        self.assertEqual(jc.parsers.sshd_conf.parse(self.f_in['sshd_t'], quiet=True),
                                                    self.f_json['sshd_t'])

    def test_sshd_T_2(self):
        """
        Test 'sshd -T' with another sample
        """
        self.assertEqual(jc.parsers.sshd_conf.parse(self.f_in['sshd_t_2'], quiet=True),
                                                    self.f_json['sshd_t_2'])

    def test_sshd_config(self):
        """
        Test 'cat sshd_config'
        """
        self.assertEqual(jc.parsers.sshd_conf.parse(self.f_in['sshd_config'], quiet=True),
                                                    self.f_json['sshd_config'])


if __name__ == '__main__':
    unittest.main()
