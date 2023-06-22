import os
import unittest
import json
import jc.parsers.x509_csr

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-csr.der'), 'rb') as f:
        x509_csr_der = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-csr.pem'), 'r', encoding='utf-8') as f:
        x509_csr_pem = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-csr-windows.pem'), 'r', encoding='utf-8') as f:
        x509_csr_windows_pem = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-csr-der.json'), 'r', encoding='utf-8') as f:
        x509_csr_der_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-csr.json'), 'r', encoding='utf-8') as f:
        x509_csr_pem_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-csr-windows.json'), 'r', encoding='utf-8') as f:
        x509_csr_windows_pem_json = json.loads(f.read())


    def test_x509_csr_nodata(self):
        """
        Test 'x509_csr' with no data
        """
        self.assertEqual(jc.parsers.x509_csr.parse('', quiet=True), [])

    def test_x509_csr_der(self):
        """
        Test csr file in DER format
        """
        self.assertEqual(jc.parsers.x509_csr.parse(self.x509_csr_der, quiet=True), self.x509_csr_der_json)

    def test_x509_csr_pem(self):
        """
        Test csr file in PEM format
        """
        self.assertEqual(jc.parsers.x509_csr.parse(self.x509_csr_pem, quiet=True), self.x509_csr_pem_json)

    def test_x509_csr_windows(self):
        """
        Test Windows csr file in PEM format
        """
        self.maxDiff = None
        self.assertEqual(jc.parsers.x509_csr.parse(self.x509_csr_windows_pem, quiet=True), self.x509_csr_windows_pem_json)


if __name__ == '__main__':
    unittest.main()
