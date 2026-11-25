import os
import time
import unittest
import json
import jc.parsers.x509_cert
from jc.parsers.asn1crypto import x509

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-general-names.pem'), 'r', encoding='utf-8') as f:
        x509_cert_general_names = f.read()

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/x509-cert-general-names.json'), 'r', encoding='utf-8') as f:
        x509_cert_general_names_json = json.loads(f.read())

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


    def _extensions(self, data):
        """Return the extensions of the first certificate, by extn_id"""
        result = jc.parsers.x509_cert.parse(data, quiet=True)
        return {e['extn_id']: e for e in result[0]['tbs_certificate']['extensions']}

    def test_x509_cert_general_names(self):
        """
        Test 'cat x509-cert-general-names.pem' (GeneralNames of several types in many extensions)
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_general_names, quiet=True), self.x509_cert_general_names_json)

    def test_x509_cert_general_names_raw(self):
        """
        Test 'cat x509-cert-general-names.pem' raw output also has the GeneralName types
        """
        self.assertEqual(jc.parsers.x509_cert.parse(self.x509_cert_general_names, raw=True, quiet=True), self.x509_cert_general_names_json)

    def test_x509_cert_san_general_names(self):
        """
        Test 'cat x509-cert-general-names.pem' subject_alt_name keeps each GeneralName type next to the value
        """
        directory_name = {
            'country_name': 'US',
            'organization_name': 'Example Org',
            'common_name': 'Directory Name'
        }
        san = self._extensions(self.x509_cert_general_names)['subject_alt_name']
        self.assertEqual(san['extn_value'], [
            'www.example.com',
            'admin@example.com',
            'https://example.com/',
            '192.0.2.10',
            '2001:db8::10',
            directory_name,
            '1.2.3.4',
            {'type_id': '1.3.6.1.4.1.311.20.2.3', 'value': 'user@example.net'}
        ])
        self.assertEqual(san['extn_value_general_names'], [
            {'type': 'dns_name', 'value': 'www.example.com'},
            {'type': 'rfc822_name', 'value': 'admin@example.com'},
            {'type': 'uniform_resource_identifier', 'value': 'https://example.com/'},
            {'type': 'ip_address', 'value': '192.0.2.10'},
            {'type': 'ip_address', 'value': '2001:db8::10'},
            {'type': 'directory_name', 'value': directory_name},
            {'type': 'registered_id', 'value': '1.2.3.4'},
            {'type': 'other_name', 'value': {'type_id': '1.3.6.1.4.1.311.20.2.3', 'value': 'user@example.net'}}
        ])
        self.assertEqual(list(san), ['extn_id', 'critical', 'extn_value', 'extn_value_general_names'])
        self.assertIs(type(san['extn_value'][0]), str)

    def test_x509_cert_ian_aia_sia_general_names(self):
        """
        Test 'cat x509-cert-general-names.pem' issuer_alt_name, authority_information_access and subject_information_access types
        """
        directory_name = {
            'country_name': 'US',
            'organization_name': 'Example Org',
            'common_name': 'Directory Name'
        }
        ext = self._extensions(self.x509_cert_general_names)
        self.assertEqual(ext['issuer_alt_name']['extn_value'], ['ca.example.net', 'ca@example.net'])
        self.assertEqual(ext['issuer_alt_name']['extn_value_general_names'], [
            {'type': 'dns_name', 'value': 'ca.example.net'},
            {'type': 'rfc822_name', 'value': 'ca@example.net'}
        ])
        self.assertEqual(ext['authority_information_access']['extn_value'], [
            {'access_method': 'ocsp', 'access_location': 'http://ocsp.example.com/', 'access_location_type': 'uniform_resource_identifier'},
            {'access_method': 'ca_issuers', 'access_location': 'http://example.com/ca.crt', 'access_location_type': 'uniform_resource_identifier'},
            {'access_method': 'ca_issuers', 'access_location': directory_name, 'access_location_type': 'directory_name'}
        ])
        self.assertEqual(ext['subject_information_access']['extn_value'], [
            {'access_method': 'ca_repository', 'access_location': 'http://example.com/repo/', 'access_location_type': 'uniform_resource_identifier'},
            {'access_method': 'ca_repository', 'access_location': 'repo.example.com', 'access_location_type': 'dns_name'}
        ])

    def test_x509_cert_crl_dp_general_names(self):
        """
        Test 'cat x509-cert-general-names.pem' crl_distribution_points and freshest_crl types
        """
        directory_name = {
            'country_name': 'US',
            'organization_name': 'Example Org',
            'common_name': 'Directory Name'
        }
        ext = self._extensions(self.x509_cert_general_names)
        self.assertEqual(ext['crl_distribution_points']['extn_value'], [
            {
                'distribution_point': ['http://example.com/ca.crl', 'crl@example.com'],
                'distribution_point_general_names': [
                    {'type': 'uniform_resource_identifier', 'value': 'http://example.com/ca.crl'},
                    {'type': 'rfc822_name', 'value': 'crl@example.com'}
                ],
                'reasons': None,
                'crl_issuer': [directory_name],
                'crl_issuer_general_names': [
                    {'type': 'directory_name', 'value': directory_name}
                ]
            }
        ])
        self.assertEqual(ext['freshest_crl']['extn_value'], [
            {
                'distribution_point': ['http://example.com/delta.crl'],
                'distribution_point_general_names': [
                    {'type': 'uniform_resource_identifier', 'value': 'http://example.com/delta.crl'}
                ],
                'reasons': None,
                'crl_issuer': None
            },
            {
                'distribution_point': ['delta.example.com'],
                'distribution_point_general_names': [
                    {'type': 'dns_name', 'value': 'delta.example.com'}
                ],
                'reasons': None,
                'crl_issuer': None
            }
        ])

    def test_x509_cert_name_constraints_aki_general_names(self):
        """
        Test 'cat x509-cert-general-names.pem' name_constraints base types and authority_key_identifier issuer types
        """
        directory_name = {
            'country_name': 'US',
            'organization_name': 'Example Org',
            'common_name': 'Directory Name'
        }
        ext = self._extensions(self.x509_cert_general_names)
        self.assertEqual(ext['name_constraints']['extn_value'], {
            'permitted_subtrees': [
                {'base': 'example.com', 'base_type': 'dns_name', 'minimum': 0, 'maximum': None},
                {'base': 'example.com', 'base_type': 'rfc822_name', 'minimum': 0, 'maximum': None},
                {'base': '192.0.2.0/24', 'base_type': 'ip_address', 'minimum': 0, 'maximum': None}
            ],
            'excluded_subtrees': [
                {'base': 'example.net', 'base_type': 'uniform_resource_identifier', 'minimum': 0, 'maximum': None},
                {'base': directory_name, 'base_type': 'directory_name', 'minimum': 0, 'maximum': None}
            ]
        })
        self.assertEqual(list(ext['name_constraints']['extn_value']['permitted_subtrees'][0]), ['base', 'base_type', 'minimum', 'maximum'])
        issuer = {'common_name': 'General Names Test CA', 'organization_name': 'Example Org'}
        self.assertEqual(ext['authority_key_identifier']['extn_value'], {
            'key_identifier': None,
            'authority_cert_issuer': [issuer],
            'authority_cert_issuer_general_names': [
                {'type': 'directory_name', 'value': issuer}
            ],
            'authority_cert_serial_number': 4097
        })

    def test_x509_cert_letsencrypt_general_names(self):
        """
        Test 'cat x509-letsencrypt.pem' keeps the existing values and adds the GeneralName types
        """
        ext = self._extensions(self.x509_letsencrypt)
        san = ext['subject_alt_name']
        self.assertEqual(san['extn_value'][0], 'baffl.ca')
        self.assertEqual(len(san['extn_value_general_names']), len(san['extn_value']))
        self.assertEqual(san['extn_value_general_names'][0], {'type': 'dns_name', 'value': 'baffl.ca'})
        self.assertEqual([i['value'] for i in san['extn_value_general_names']], san['extn_value'])
        self.assertEqual(ext['authority_information_access']['extn_value'][0], {
            'access_method': 'ocsp',
            'access_location': 'http://r3.o.lencr.org',
            'access_location_type': 'uniform_resource_identifier'
        })
        # no GeneralNames in this authority_key_identifier: no new key
        self.assertEqual(list(ext['authority_key_identifier']['extn_value']), ['key_identifier', 'authority_cert_issuer', 'authority_cert_serial_number'])

    def test_x509_cert_x400_address_general_name(self):
        """
        Test an x400_address GeneralName gets its type
        """
        names = x509.GeneralNames([
            x509.GeneralName(name='x400_address', value={
                'built_in_standard_attributes': {
                    'country_name': x509.CountryName(name='x121_dcc_code', value='123'),
                    'organization_name': 'Example Org'
                }
            })
        ])
        names = x509.GeneralNames.load(names.dump())
        result = jc.parsers.x509_cert._fix_objects({'names': names.native})
        self.assertEqual(result['names'][0]['built_in_standard_attributes']['organization_name'], 'Example Org')
        self.assertEqual(result['names_general_names'], [{'type': 'x400_address', 'value': result['names'][0]}])


if __name__ == '__main__':
    unittest.main()
