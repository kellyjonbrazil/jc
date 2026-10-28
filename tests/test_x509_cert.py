import os
import time
import unittest
import json
import jc.parsers.x509_cert

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def _parse_in_tz(parser, data, tz):
    """Parse data with the TZ environment variable set to tz"""
    old_tz = os.environ.get('TZ')
    os.environ['TZ'] = tz
    time.tzset()
    try:
        return parser.parse(data, quiet=True)
    finally:
        if old_tz is None:
            del os.environ['TZ']
        else:
            os.environ['TZ'] = old_tz
        time.tzset()


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-ca-cert.der'), 'rb') as f:
        x509_ca_cert = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-and-key.pem'), 'r', encoding='utf-8') as f:
        x509_cert_and_key_pem = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-letsencrypt.pem'), 'r', encoding='utf-8') as f:
        x509_letsencrypt = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-multi-cert.pem'), 'r', encoding='utf-8') as f:
        x509_multi_cert = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-string-serialnumber.der'), 'rb') as f:
        x509_string_serialnumber = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-bad-email.pem'), 'rb') as f:
        x509_cert_bad_email = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-superfluous-bits.pem'), 'rb') as f:
        x509_cert_superfluous_bits = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-negative-serial.pem'), 'rb') as f:
        x509_cert_negative_serial = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-bad-email2.der'), 'rb') as f:
        x509_cert_bad_email2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-trusted-label.pem'), 'rb') as f:
        x509_cert_trusted_label = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-x509-label.pem'), 'rb') as f:
        x509_cert_x509_label = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-no-zone.pem'), 'rb') as f:
        x509_cert_no_zone = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-ca-cert.json'), 'r', encoding='utf-8') as f:
        x509_ca_cert_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-and-key.json'), 'r', encoding='utf-8') as f:
        x509_cert_and_key_pem_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-letsencrypt.json'), 'r', encoding='utf-8') as f:
        x509_letsencrypt_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-multi-cert.json'), 'r', encoding='utf-8') as f:
        x509_multi_cert_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-string-serialnumber.json'), 'r', encoding='utf-8') as f:
        x509_string_serialnumber_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-bad-email.json'), 'r', encoding='utf-8') as f:
        x509_cert_bad_email_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-superfluous-bits.json'), 'r', encoding='utf-8') as f:
        x509_cert_superfluous_bits_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-negative-serial.json'), 'r', encoding='utf-8') as f:
        x509_cert_negative_serial_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-bad-email2.json'), 'r', encoding='utf-8') as f:
        x509_cert_bad_email2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-trusted-label.json'), 'r', encoding='utf-8') as f:
        x509_cert_trusted_label_json = json.loads(f.read())


    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-no-zone.json'), 'r', encoding='utf-8') as f:
        x509_cert_no_zone_json = json.loads(f.read())

    def test_x509_cert_nodata(self):
        """
        Test 'x509_cert' with no data
        """
        self.assertEqual(jc.parsers.x509_cert.parse('', quiet=True), [])

    def test_x509_ca_cert(self):
        """
        Test 'cat x509-ca-cert.der' (CA cert in DER format)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_ca_cert, quiet=True), self.x509_ca_cert_json)

    def test_x509_cert_and_key(self):
        """
        Test 'cat x509-cert-and-key.pem' (combo cert and key file in PEM format)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_and_key_pem, quiet=True), self.x509_cert_and_key_pem_json)

    def test_x509_letsencrypt(self):
        """
        Test 'cat x509-letsencrypt.pem' (letsencrypt cert in PEM format)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_letsencrypt, quiet=True), self.x509_letsencrypt_json)

    def test_x509_multi_cert(self):
        """
        Test 'cat x509-multi-cert.pem' (PEM file with multiple certificates)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_multi_cert, quiet=True), self.x509_multi_cert_json)

    def test_x509_string_serialnumber(self):
        """
        Test 'cat x509-string-serialnumber.der' (DER file with string serial numbers)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_multi_cert, quiet=True), self.x509_multi_cert_json)

    def test_x509_cert_bad_email(self):
        """
        Test 'cat x509-cert-bad-email.pem' (PEM file with a non-compliant email address)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_bad_email, quiet=True), self.x509_cert_bad_email_json)

    def test_x509_cert_superfluous_bits(self):
        """
        Test 'cat x509-cert-superfluous-bits.pem' (PEM file with more bits set for the keyUsage extension than defined by the RFC)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_superfluous_bits, quiet=True),
                         self.x509_cert_superfluous_bits_json)
    def test_x509_cert_negative_serial(self):
        """
        Test 'cat x509-cert-bad-email.pem' (PEM file with a non-compliant email address)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_negative_serial, quiet=True), self.x509_cert_negative_serial_json)

    def test_x509_cert_bad_email2(self):
        """
        Test 'cat x509-cert-bad-email2.der' (DER file with a non-compliant email address - IDNA2008 encoded)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_bad_email2, quiet=True), self.x509_cert_bad_email2_json)

    def test_x509_cert_trusted_label(self):
        """
        Test 'cat x509-cert-trusted-label.pem' (PEM block labeled TRUSTED CERTIFICATE)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_trusted_label, quiet=True), self.x509_cert_trusted_label_json)

    def test_x509_cert_x509_label(self):
        """
        Test 'cat x509-cert-x509-label.pem' (PEM block labeled X509 CERTIFICATE)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_x509_label, quiet=True), self.x509_cert_trusted_label_json)

    def test_x509_cert_no_zone(self):
        """
        Test 'cat x509-cert-no-zone.pem' (GeneralizedTime without a time zone)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_no_zone, quiet=True), self.x509_cert_no_zone_json)

    @unittest.skipUnless(hasattr(time, 'tzset'), 'time.tzset() is not available')
    def test_x509_cert_no_zone_tz(self):
        """
        Test 'cat x509-cert-no-zone.pem' (GeneralizedTime without a time zone) is read as UTC in any time zone
        """
        for tz in ('UTC', 'Asia/Tokyo'):
            result = _parse_in_tz(jc.parsers.x509_cert, self.x509_cert_no_zone, tz)
            validity = result[0]['tbs_certificate']['validity']
            self.assertEqual(validity['not_before'], 1577836800)
            self.assertEqual(validity['not_after'], 2208988800)
            self.assertEqual(validity['not_after_iso'], '2040-01-01T00:00:00+00:00')
            self.assertEqual(result, self.x509_cert_no_zone_json)


if __name__ == '__main__':
    unittest.main()
