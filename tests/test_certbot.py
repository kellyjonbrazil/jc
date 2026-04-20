import os
import unittest
import json
from typing import Dict
from jc.parsers.certbot import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        fixtures = {
            'account': (
                'fixtures/generic/certbot-account.out',
                'fixtures/generic/certbot-account.json'),
            'certificates': (
                'fixtures/generic/certbot-certs.out',
                'fixtures/generic/certbot-certs.json'),
            'certificates-cert-name': (
                'fixtures/generic/certbot-certs-cert-name.out',
                'fixtures/generic/certbot-certs-cert-name.json')

        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_certbot_nodata(self):
        """
        Test 'certbot' with no data
        """
        self.assertEqual(parse('', quiet=True), {})


    def test_certbot_certificates(self):
        """
        Test 'certbot certificates'
        """
        self.assertEqual(
            parse(self.f_in['certificates'], quiet=True),
            self.f_json['certificates']
        )

    def test_certbot_certificates_cert_name(self):
        """
        Test 'certbot certificates' with cert name
        """
        self.assertEqual(
            parse(self.f_in['certificates-cert-name'], quiet=True),
            self.f_json['certificates-cert-name']
        )
    def test_certbot_account(self):
        """
        Test 'certbot account'
        """
        self.assertEqual(
            parse(self.f_in['account'], quiet=True),
            self.f_json['account']
        )

if __name__ == '__main__':
    unittest.main()
