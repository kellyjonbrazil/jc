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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-general-names.pem'), 'r', encoding='utf-8') as f:
        x509_crl_general_names_pem = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-der.json'), 'r', encoding='utf-8') as f:
        x509_crl_der_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl.json'), 'r', encoding='utf-8') as f:
        x509_crl_pem_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-no-zone.json'), 'r', encoding='utf-8') as f:
        x509_crl_no_zone_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-multi.json'), 'r', encoding='utf-8') as f:
        x509_crl_multi_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-crl-general-names.json'), 'r', encoding='utf-8') as f:
        x509_crl_general_names_json = json.loads(f.read())


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

    def test_x509_crl_general_names(self):
        """
        Test 'cat x509-crl-general-names.pem' (GeneralNames in CRL and CRL entry extensions)
        """
        result = jc.parsers.x509_crl.parse(self.x509_crl_general_names_pem, quiet=True)
        self.assertEqual(result, self.x509_crl_general_names_json)
        tbs = result[0]['tbs_cert_list']
        ext = {e['extn_id']: e for e in tbs['crl_extensions']}
        self.assertEqual(ext['issuer_alt_name']['extn_value'], ['ca.example.net', 'http://example.net/'])
        self.assertEqual(ext['issuer_alt_name']['extn_value_general_names'], [
            {'type': 'dns_name', 'value': 'ca.example.net'},
            {'type': 'uniform_resource_identifier', 'value': 'http://example.net/'}
        ])
        idp = ext['issuing_distribution_point']['extn_value']
        self.assertEqual(idp['distribution_point'], ['http://example.com/ca.crl', 'crl.example.com'])
        self.assertEqual(idp['distribution_point_general_names'], [
            {'type': 'uniform_resource_identifier', 'value': 'http://example.com/ca.crl'},
            {'type': 'dns_name', 'value': 'crl.example.com'}
        ])
        self.assertEqual(list(idp)[:2], ['distribution_point', 'distribution_point_general_names'])
        self.assertTrue(idp['indirect_crl'])
        entry = {e['extn_id']: e for e in tbs['revoked_certificates'][0]['crl_entry_extensions']}
        other_ca = {'country_name': 'US', 'organization_name': 'Example Org', 'common_name': 'Other Example CA'}
        self.assertEqual(entry['certificate_issuer'], {
            'extn_id': 'certificate_issuer',
            'critical': True,
            'extn_value': [other_ca, 'other-ca.example.net'],
            'extn_value_general_names': [
                {'type': 'directory_name', 'value': other_ca},
                {'type': 'dns_name', 'value': 'other-ca.example.net'}
            ]
        })
        self.assertEqual(entry['crl_reason']['extn_value'], 'key_compromise')

    def test_x509_crl_der_issuing_distribution_point(self):
        """
        Test 'cat x509-crl.der' issuing_distribution_point gets the GeneralName types
        """
        result = jc.parsers.x509_crl.parse(self.x509_crl_der, quiet=True)
        ext = {e['extn_id']: e for e in result[0]['tbs_cert_list']['crl_extensions']}
        idp = ext['issuing_distribution_point']['extn_value']
        self.assertEqual(idp['distribution_point'], ['http://www.sk.ee/repository/crls/eid2011.crl'])
        self.assertEqual(idp['distribution_point_general_names'], [
            {'type': 'uniform_resource_identifier', 'value': 'http://www.sk.ee/repository/crls/eid2011.crl'}
        ])


if __name__ == '__main__':
    unittest.main()
