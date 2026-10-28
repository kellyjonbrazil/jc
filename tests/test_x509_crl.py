import os
import time
import unittest
import json
import jc.parsers.x509_crl
from jc.exceptions import ParseError

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
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl.der'), 'rb') as f:
        x509_crl_der = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl.pem'), 'r', encoding='utf-8') as f:
        x509_crl_pem = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-no-zone.pem'), 'r', encoding='utf-8') as f:
        x509_crl_no_zone_pem = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-multi.pem'), 'r', encoding='utf-8') as f:
        x509_crl_multi_pem = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-der.json'), 'r', encoding='utf-8') as f:
        x509_crl_der_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl.json'), 'r', encoding='utf-8') as f:
        x509_crl_pem_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-no-zone.json'), 'r', encoding='utf-8') as f:
        x509_crl_no_zone_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-multi.json'), 'r', encoding='utf-8') as f:
        x509_crl_multi_json = json.loads(f.read())


    def test_x509_crl_nodata(self):
        """
        Test 'x509_crl' with no data
        """
        self.assertEqual(jc.parsers.x509_crl.parse('', quiet=True), [])

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

    def test_x509_crl_der_single(self):
        """
        Test crl file in DER format returns a list with one crl
        """
        result = jc.parsers.x509_crl.parse(self.x509_crl_der, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['tbs_cert_list']['issuer']['common_name'], 'EID-SK 2011')

    def test_x509_crl_multi(self):
        """
        Test 'cat x509-crl-multi.pem' (PEM file with two crls)
        """
        result = jc.parsers.x509_crl.parse(self.x509_crl_multi_pem, quiet=True)
        self.assertEqual(result, self.x509_crl_multi_json)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['tbs_cert_list']['issuer']['common_name'], 'Partner CA')
        self.assertIsNone(result[0]['tbs_cert_list']['revoked_certificates'])
        self.assertEqual(result[1]['tbs_cert_list']['issuer']['common_name'], 'Staff CA')
        self.assertEqual(result[1]['tbs_cert_list']['revoked_certificates'][0]['user_certificate'], 6699)

    def test_x509_crl_pem_other_blocks(self):
        """
        Test crl file in PEM format with a block of another type before the crl
        """
        data = '-----BEGIN CERTIFICATE-----\nAAAA\n-----END CERTIFICATE-----\n' + self.x509_crl_pem
        self.assertEqual(jc.parsers.x509_crl.parse(data, quiet=True), self.x509_crl_pem_json)

    def test_x509_crl_pem_no_crl(self):
        """
        Test PEM file without a crl block
        """
        data = '-----BEGIN CERTIFICATE-----\nAAAA\n-----END CERTIFICATE-----\n'
        with self.assertRaises(ParseError):
            jc.parsers.x509_crl.parse(data, quiet=True)

    def test_x509_crl_no_zone(self):
        """
        Test 'cat x509-crl-no-zone.pem' (GeneralizedTime without a time zone)
        """
        self.assertEqual(jc.parsers.x509_crl.parse(self.x509_crl_no_zone_pem, quiet=True), self.x509_crl_no_zone_json)

    @unittest.skipUnless(hasattr(time, 'tzset'), 'time.tzset() is not available')
    def test_x509_crl_no_zone_tz(self):
        """
        Test 'cat x509-crl-no-zone.pem' (GeneralizedTime without a time zone) is read as UTC in any time zone
        """
        for tz in ('UTC', 'Asia/Tokyo'):
            result = _parse_in_tz(jc.parsers.x509_crl, self.x509_crl_no_zone_pem, tz)
            tbs = result[0]['tbs_cert_list']
            self.assertEqual(tbs['this_update'], 2208988800)
            self.assertEqual(tbs['this_update_iso'], '2040-01-01T00:00:00+00:00')
            self.assertEqual(tbs['next_update'], 2209075200)
            self.assertEqual(tbs['next_update_iso'], '2040-01-02T00:00:00+00:00')
            self.assertEqual(tbs['revoked_certificates'][0]['revocation_date'], 1361182932)
            self.assertEqual(result, self.x509_crl_no_zone_json)


if __name__ == '__main__':
    unittest.main()
