import os
import unittest
import json
import jc.parsers.x509_crl

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl.der'), 'rb') as f:
        x509_crl_der = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl.pem'), 'r', encoding='utf-8') as f:
        x509_crl_pem = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-der.json'), 'r', encoding='utf-8') as f:
        x509_crl_der_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl.json'), 'r', encoding='utf-8') as f:
        x509_crl_pem_json = json.loads(f.read())


    def test_x509_crl_nodata(self):
        """
        Test 'x509_crl' with no data
        """
        self.assertEqual(jc.parsers.x509_crl.parse('', quiet=True), {})

    def test_x509_crl_der(self):
        """
        Test crl file in DER format
        """
        self.assertEqual(jc.parsers.x509_crl.parse(self.x509_crl_der, quiet=True), self.x509_crl_der_json)

    def test_x509_crl_pem(self):
        """
        Test crl file in PEM format
        """
        self.assertEqual(jc.parsers.x509_crl.parse(self.x509_crl_pem, quiet=True), self.x509_crl_pem_json)


if __name__ == '__main__':
    unittest.main()
