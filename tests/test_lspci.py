import os
import unittest
import json
from typing import Dict
import jc.parsers.lspci

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'ubuntu_20_10_lspci_mmv': (
                'fixtures/ubuntu-20.10/lspci-mmv.out',
                'fixtures/ubuntu-20.10/lspci-mmv.json'),
            'ubuntu_20_10_lspci_nmmv': (
                'fixtures/ubuntu-20.10/lspci-nmmv.out',
                'fixtures/ubuntu-20.10/lspci-nmmv.json'),
            'ubuntu_20_10_lspci_nnmmv': (
                'fixtures/ubuntu-20.10/lspci-nnmmv.out',
                'fixtures/ubuntu-20.10/lspci-nnmmv.json'),
            'ubuntu_24_04_lspci_vvvnn_a100': (
                'fixtures/ubuntu-24.04/lspci-vvvnn-a100.out',
                'fixtures/ubuntu-24.04/lspci-vvvnn-a100.json'),
            'ubuntu_24_04_lspci_vvvnn_wsl': (
                'fixtures/ubuntu-24.04/lspci-vvvnn-wsl.out',
                'fixtures/ubuntu-24.04/lspci-vvvnn-wsl.json'),
            'ubuntu_24_04_lspci_vvvnn_mi300': (
                'fixtures/ubuntu-24.04/lspci-vvvnn-mi300.out',
                'fixtures/ubuntu-24.04/lspci-vvvnn-mi300.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_lspci_nodata(self):
        """
        Test 'lspci' with no data
        """
        self.assertEqual(jc.parsers.lspci.parse('', quiet=True), [])

    def test_lspci_mmv_ubuntu_20_10(self):
        """
        Test 'lspci -mmv' on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.lspci.parse(self.f_in['ubuntu_20_10_lspci_mmv'], quiet=True),
                                                self.f_json['ubuntu_20_10_lspci_mmv'])

    def test_lspci_nmmv_ubuntu_20_10(self):
        """
        Test 'lspci -nmmv' on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.lspci.parse(self.f_in['ubuntu_20_10_lspci_nmmv'], quiet=True),
                                                self.f_json['ubuntu_20_10_lspci_nmmv'])

    def test_lspci_nnmmv_ubuntu_20_10(self):
        """
        Test 'lspci -nnmmv' on Ubuntu 20.10
        """
        self.assertEqual(jc.parsers.lspci.parse(self.f_in['ubuntu_20_10_lspci_nnmmv'], quiet=True),
                                                self.f_json['ubuntu_20_10_lspci_nnmmv'])

    def test_lspci_vvvnn_ubuntu_24_04(self):
        """
        Test 'lspci -vvvnn' fixtures on Ubuntu 24.04
        """
        for fixture in (
            'ubuntu_24_04_lspci_vvvnn_a100',
            'ubuntu_24_04_lspci_vvvnn_wsl',
            'ubuntu_24_04_lspci_vvvnn_mi300'
        ):
            with self.subTest(fixture=fixture):
                self.assertEqual(
                    jc.parsers.lspci.parse(self.f_in[fixture], quiet=True),
                    self.f_json[fixture]
                )


if __name__ == '__main__':
    unittest.main()
