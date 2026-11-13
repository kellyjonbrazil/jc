import os
import unittest
import json
from typing import Dict
from jc.parsers.certbot import parse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

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
    def test_certbot_certificates_validity_text(self):
        """
        Test 'certbot certificates' with INVALID validity and parentheses in
        the validity text
        """
        data = (
            'Found the following certs:\n'
            '  Certificate Name: old.example.com\n'
            '    Serial Number: 1a2b\n'
            '    Expiry Date: 2023-05-11 01:33:10+00:00 (INVALID: EXPIRED)\n'
            '  Certificate Name: new.example.com\n'
            '    Serial Number: 3c4d\n'
            '    Expiry Date: 2023-06-12 01:35:30+00:00 (VALID: 1 hour(s))\n'
            '  Certificate Name: test.example.com\n'
            '    Expiry Date: 2023-06-12 01:35:30+00:00 (INVALID: TEST_CERT)\n'
        )
        result = parse(data, quiet=True)['certificates']
        self.assertEqual(result[0]['validity'], 'INVALID: EXPIRED')
        self.assertEqual(result[1]['validity'], '1 hour(s)')
        self.assertEqual(result[1]['expiration_date'], '2023-06-12 01:35:30+00:00')
        self.assertEqual(result[2]['validity'], 'INVALID: TEST_CERT')


if __name__ == '__main__':
    unittest.main()
