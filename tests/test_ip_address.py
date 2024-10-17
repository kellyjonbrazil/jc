import unittest
import json
import jc.parsers.ip_address


class MyTests(unittest.TestCase):

    def test_ip_address_nodata(self):
        """
        Test 'ip_address' with no data
        """
        self.assertEqual(jc.parsers.ip_address.parse('', quiet=True), {})


    def test_ip_address_ipv4(self):
        """
        Test ipv4 address string
        """
        data = r'192.168.1.35'
        expected = json.loads(r'''{"version":4,"max_prefix_length":32,"ip":"192.168.1.35","ip_compressed":"192.168.1.35","ip_exploded":"192.168.1.35","ip_split":["192","168","1","35"],"scope_id":null,"ipv4_mapped":null,"six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"35.1.168.192.in-addr.arpa","network":"192.168.1.35","broadcast":"192.168.1.35","hostmask":"0.0.0.0","netmask":"255.255.255.255","cidr_netmask":32,"hosts":1,"first_host":"192.168.1.35","last_host":"192.168.1.35","is_multicast":false,"is_private":true,"is_global":false,"is_link_local":false,"is_loopback":false,"is_reserved":false,"is_unspecified":false,"int":{"ip":3232235811,"network":3232235811,"broadcast":3232235811,"first_host":3232235811,"last_host":3232235811},"hex":{"ip":"c0:a8:01:23","network":"c0:a8:01:23","broadcast":"c0:a8:01:23","hostmask":"00:00:00:00","netmask":"ff:ff:ff:ff","first_host":"c0:a8:01:23","last_host":"c0:a8:01:23"},"bin":{"ip":"11000000101010000000000100100011","network":"11000000101010000000000100100011","broadcast":"11000000101010000000000100100011","hostmask":"00000000000000000000000000000000","netmask":"11111111111111111111111111111111","first_host":"11000000101010000000000100100011","last_host":"11000000101010000000000100100011"}}''')
        self.assertEqual(jc.parsers.ip_address.parse(data, quiet=True), expected)


    def test_ip_address_ipv4_cidr(self):
        """
        Test CIDR ipv4 address string
        """
        data = r'192.168.2.10/24'
        expected = json.loads(r'''{"version":4,"max_prefix_length":32,"ip":"192.168.2.10","ip_compressed":"192.168.2.10","ip_exploded":"192.168.2.10","ip_split":["192","168","2","10"],"scope_id":null,"ipv4_mapped":null,"six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"10.2.168.192.in-addr.arpa","network":"192.168.2.0","broadcast":"192.168.2.255","hostmask":"0.0.0.255","netmask":"255.255.255.0","cidr_netmask":24,"hosts":254,"first_host":"192.168.2.1","last_host":"192.168.2.254","is_multicast":false,"is_private":true,"is_global":false,"is_link_local":false,"is_loopback":false,"is_reserved":false,"is_unspecified":false,"int":{"ip":3232236042,"network":3232236032,"broadcast":3232236287,"first_host":3232236033,"last_host":3232236286},"hex":{"ip":"c0:a8:02:0a","network":"c0:a8:02:00","broadcast":"c0:a8:02:ff","hostmask":"00:00:00:ff","netmask":"ff:ff:ff:00","first_host":"c0:a8:02:01","last_host":"c0:a8:02:fe"},"bin":{"ip":"11000000101010000000001000001010","network":"11000000101010000000001000000000","broadcast":"11000000101010000000001011111111","hostmask":"00000000000000000000000011111111","netmask":"11111111111111111111111100000000","first_host":"11000000101010000000001000000001","last_host":"11000000101010000000001011111110"}}''')
        self.assertEqual(jc.parsers.ip_address.parse(data, quiet=True), expected)


    def test_ip_address_ipv4_dotnetmask(self):
        """
        Test ipv4 address with a dotted netmask string
        """
        data = r'192.168.0.1/255.255.128.0'
        expected = json.loads(r'''{"version":4,"max_prefix_length":32,"ip":"192.168.0.1","ip_compressed":"192.168.0.1","ip_exploded":"192.168.0.1","ip_split":["192","168","0","1"],"scope_id":null,"ipv4_mapped":null,"six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"1.0.168.192.in-addr.arpa","network":"192.168.0.0","broadcast":"192.168.127.255","hostmask":"0.0.127.255","netmask":"255.255.128.0","cidr_netmask":17,"hosts":32766,"first_host":"192.168.0.1","last_host":"192.168.127.254","is_multicast":false,"is_private":true,"is_global":false,"is_link_local":false,"is_loopback":false,"is_reserved":false,"is_unspecified":false,"int":{"ip":3232235521,"network":3232235520,"broadcast":3232268287,"first_host":3232235521,"last_host":3232268286},"hex":{"ip":"c0:a8:00:01","network":"c0:a8:00:00","broadcast":"c0:a8:7f:ff","hostmask":"00:00:7f:ff","netmask":"ff:ff:80:00","first_host":"c0:a8:00:01","last_host":"c0:a8:7f:fe"},"bin":{"ip":"11000000101010000000000000000001","network":"11000000101010000000000000000000","broadcast":"11000000101010000111111111111111","hostmask":"00000000000000000111111111111111","netmask":"11111111111111111000000000000000","first_host":"11000000101010000000000000000001","last_host":"11000000101010000111111111111110"}}''')
        self.assertEqual(jc.parsers.ip_address.parse(data, quiet=True), expected)


    def test_ip_address_ipv4_integer(self):
        """
        Test ipv4 address integer string
        """
        data = r'3232236042'
        expected = json.loads(r'''{"version":4,"max_prefix_length":32,"ip":"192.168.2.10","ip_compressed":"192.168.2.10","ip_exploded":"192.168.2.10","ip_split":["192","168","2","10"],"scope_id":null,"ipv4_mapped":null,"six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"10.2.168.192.in-addr.arpa","network":"192.168.2.10","broadcast":"192.168.2.10","hostmask":"0.0.0.0","netmask":"255.255.255.255","cidr_netmask":32,"hosts":1,"first_host":"192.168.2.10","last_host":"192.168.2.10","is_multicast":false,"is_private":true,"is_global":false,"is_link_local":false,"is_loopback":false,"is_reserved":false,"is_unspecified":false,"int":{"ip":3232236042,"network":3232236042,"broadcast":3232236042,"first_host":3232236042,"last_host":3232236042},"hex":{"ip":"c0:a8:02:0a","network":"c0:a8:02:0a","broadcast":"c0:a8:02:0a","hostmask":"00:00:00:00","netmask":"ff:ff:ff:ff","first_host":"c0:a8:02:0a","last_host":"c0:a8:02:0a"},"bin":{"ip":"11000000101010000000001000001010","network":"11000000101010000000001000001010","broadcast":"11000000101010000000001000001010","hostmask":"00000000000000000000000000000000","netmask":"11111111111111111111111111111111","first_host":"11000000101010000000001000001010","last_host":"11000000101010000000001000001010"}}''')
        self.assertEqual(jc.parsers.ip_address.parse(data, quiet=True), expected)


    def test_ip_address_ipv6(self):
        """
        Test ipv6 address string
        """
        data = r'127:0:de::1'
        expected = json.loads(r'''{"version":6,"max_prefix_length":128,"ip":"127:0:de::1","ip_compressed":"127:0:de::1","ip_exploded":"0127:0000:00de:0000:0000:0000:0000:0001","ip_split":["0127","0000","00de","0000","0000","0000","0000","0001"],"scope_id":null,"ipv4_mapped":null,"six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.e.d.0.0.0.0.0.0.7.2.1.0.ip6.arpa","network":"127:0:de::1","broadcast":"127:0:de::1","hostmask":"::","netmask":"ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff","cidr_netmask":128,"hosts":1,"first_host":"127:0:de::1","last_host":"127:0:de::1","is_multicast":false,"is_private":false,"is_global":true,"is_link_local":false,"is_loopback":false,"is_reserved":true,"is_unspecified":false,"int":{"ip":1531727573536155682370944093904699393,"network":1531727573536155682370944093904699393,"broadcast":1531727573536155682370944093904699393,"first_host":1531727573536155682370944093904699393,"last_host":1531727573536155682370944093904699393},"hex":{"ip":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","network":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","broadcast":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","hostmask":"00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00","netmask":"ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","first_host":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","last_host":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01"},"bin":{"ip":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","network":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","broadcast":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","hostmask":"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","netmask":"11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111","first_host":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","last_host":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001"}}''')
        self.assertEqual(jc.parsers.ip_address.parse(data, quiet=True), expected)


    def test_ip_address_ipv6_cidr(self):
        """
        Test CIDR ipv6 address string
        """
        data = r'127:0:de::1/96'
        expected = json.loads(r'''{"version":6,"max_prefix_length":128,"ip":"127:0:de::1","ip_compressed":"127:0:de::1","ip_exploded":"0127:0000:00de:0000:0000:0000:0000:0001","ip_split":["0127","0000","00de","0000","0000","0000","0000","0001"],"scope_id":null,"ipv4_mapped":null,"six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.e.d.0.0.0.0.0.0.7.2.1.0.ip6.arpa","network":"127:0:de::","broadcast":"127:0:de::ffff:ffff","hostmask":"::ffff:ffff","netmask":"ffff:ffff:ffff:ffff:ffff:ffff::","cidr_netmask":96,"hosts":4294967294,"first_host":"127:0:de::1","last_host":"127:0:de::ffff:fffe","is_multicast":false,"is_private":false,"is_global":true,"is_link_local":false,"is_loopback":false,"is_reserved":true,"is_unspecified":false,"int":{"ip":1531727573536155682370944093904699393,"network":1531727573536155682370944093904699392,"broadcast":1531727573536155682370944098199666687,"first_host":1531727573536155682370944093904699393,"last_host":1531727573536155682370944098199666686},"hex":{"ip":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","network":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:00","broadcast":"01:27:00:00:00:de:00:00:00:00:00:00:ff:ff:ff:ff","hostmask":"00:00:00:00:00:00:00:00:00:00:00:00:ff:ff:ff:ff","netmask":"ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:00:00:00:00","first_host":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","last_host":"01:27:00:00:00:de:00:00:00:00:00:00:ff:ff:ff:fe"},"bin":{"ip":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","network":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000000","broadcast":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000011111111111111111111111111111111","hostmask":"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111","netmask":"11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000000000000000000000000","first_host":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","last_host":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000011111111111111111111111111111110"}}''')
        self.assertEqual(jc.parsers.ip_address.parse(data, quiet=True), expected)


    def test_ip_address_ipv6_cidr_scope(self):
        """
        Test CIDR ipv6 address with scope string
        """
        data = r'127:0:de::1%128aBc123/96'
        expected = json.loads(r'''{"version":6,"max_prefix_length":128,"ip":"127:0:de::1","ip_compressed":"127:0:de::1","ip_exploded":"0127:0000:00de:0000:0000:0000:0000:0001","ip_split":["0127","0000","00de","0000","0000","0000","0000","0001"],"scope_id":"128aBc123","ipv4_mapped":null,"six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.e.d.0.0.0.0.0.0.7.2.1.0.ip6.arpa","network":"127:0:de::","broadcast":"127:0:de::ffff:ffff","hostmask":"::ffff:ffff","netmask":"ffff:ffff:ffff:ffff:ffff:ffff::","cidr_netmask":96,"hosts":4294967294,"first_host":"127:0:de::1","last_host":"127:0:de::ffff:fffe","is_multicast":false,"is_private":false,"is_global":true,"is_link_local":false,"is_loopback":false,"is_reserved":true,"is_unspecified":false,"int":{"ip":1531727573536155682370944093904699393,"network":1531727573536155682370944093904699392,"broadcast":1531727573536155682370944098199666687,"first_host":1531727573536155682370944093904699393,"last_host":1531727573536155682370944098199666686},"hex":{"ip":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","network":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:00","broadcast":"01:27:00:00:00:de:00:00:00:00:00:00:ff:ff:ff:ff","hostmask":"00:00:00:00:00:00:00:00:00:00:00:00:ff:ff:ff:ff","netmask":"ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:00:00:00:00","first_host":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","last_host":"01:27:00:00:00:de:00:00:00:00:00:00:ff:ff:ff:fe"},"bin":{"ip":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","network":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000000","broadcast":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000011111111111111111111111111111111","hostmask":"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111","netmask":"11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000000000000000000000000","first_host":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","last_host":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000011111111111111111111111111111110"}}''')
        self.assertEqual(jc.parsers.ip_address.parse(data, quiet=True), expected)


    def test_ip_address_ipv6_integer(self):
        """
        Test ipv6 address integer string
        """
        data = r'1531727573536155682370944093904699393'
        expected = json.loads(r'''{"version":6,"max_prefix_length":128,"ip":"127:0:de::1","ip_compressed":"127:0:de::1","ip_exploded":"0127:0000:00de:0000:0000:0000:0000:0001","ip_split":["0127","0000","00de","0000","0000","0000","0000","0001"],"scope_id":null,"ipv4_mapped":null,"six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.e.d.0.0.0.0.0.0.7.2.1.0.ip6.arpa","network":"127:0:de::1","broadcast":"127:0:de::1","hostmask":"::","netmask":"ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff","cidr_netmask":128,"hosts":1,"first_host":"127:0:de::1","last_host":"127:0:de::1","is_multicast":false,"is_private":false,"is_global":true,"is_link_local":false,"is_loopback":false,"is_reserved":true,"is_unspecified":false,"int":{"ip":1531727573536155682370944093904699393,"network":1531727573536155682370944093904699393,"broadcast":1531727573536155682370944093904699393,"first_host":1531727573536155682370944093904699393,"last_host":1531727573536155682370944093904699393},"hex":{"ip":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","network":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","broadcast":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","hostmask":"00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00","netmask":"ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","first_host":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01","last_host":"01:27:00:00:00:de:00:00:00:00:00:00:00:00:00:01"},"bin":{"ip":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","network":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","broadcast":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","hostmask":"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","netmask":"11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111","first_host":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001","last_host":"00000001001001110000000000000000000000001101111000000000000000000000000000000000000000000000000000000000000000000000000000000001"}}''')
        self.assertEqual(jc.parsers.ip_address.parse(data, quiet=True), expected)


    def test_ip_address_ipv6_ipv4_mapped(self):
        """
        Test ipv6 address with ipv4 mapped string
        """
        # IPv4 mapped behavior changes in newer versions of python are being backported
        # to old versions so we are checking if at least one style passes

        data = r'::FFFF:192.168.1.35'
        actual = jc.parsers.ip_address.parse(data, quiet=True)
        failures = 0
        failure_msgs = []

        # New-Style IPv4 Mapped output with is_reserved=false
        expected_ipv4 = '192.168.1.35'
        expected_ipv4_exploded = '192.168.1.35'
        expected_ipv4_split = '["0000", "0000", "0000", "0000", "0000", "ffff", "192", "168", "1", "35"]'
        expected_is_reserved = 'false'
        expected = json.loads(f'''{{"version":6,"max_prefix_length":128,"ip":"::ffff:{expected_ipv4}","ip_compressed":"::ffff:{expected_ipv4}","ip_exploded":"0000:0000:0000:0000:0000:ffff:{expected_ipv4_exploded}","ip_split":{expected_ipv4_split},"scope_id":null,"ipv4_mapped":"192.168.1.35","six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"3.2.1.0.8.a.0.c.f.f.f.f.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa","network":"::ffff:{expected_ipv4}","broadcast":"::ffff:{expected_ipv4}","hostmask":"::","netmask":"ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff","cidr_netmask":128,"hosts":1,"first_host":"::ffff:{expected_ipv4}","last_host":"::ffff:{expected_ipv4}","is_multicast":false,"is_private":true,"is_global":false,"is_link_local":false,"is_loopback":false,"is_reserved":{expected_is_reserved},"is_unspecified":false,"int":{{"ip":281473913979171,"network":281473913979171,"broadcast":281473913979171,"first_host":281473913979171,"last_host":281473913979171}},"hex":{{"ip":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","network":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","broadcast":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","hostmask":"00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00","netmask":"ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","first_host":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","last_host":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23"}},"bin":{{"ip":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","network":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","broadcast":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","hostmask":"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","netmask":"11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111","first_host":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","last_host":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011"}}}}''')

        try:
            self.assertEqual(actual, expected)
        except AssertionError:
            failures += 1
            failure_msgs.append(f'New-style IPv4 Mapped is_reserved=false failure:\n  Expected:  {expected}\n  Actual:  {actual}')

        # New-Style IPv4 Mapped output with is_reserved=true
        expected_is_reserved = 'true'
        expected = json.loads(f'''{{"version":6,"max_prefix_length":128,"ip":"::ffff:{expected_ipv4}","ip_compressed":"::ffff:{expected_ipv4}","ip_exploded":"0000:0000:0000:0000:0000:ffff:{expected_ipv4_exploded}","ip_split":{expected_ipv4_split},"scope_id":null,"ipv4_mapped":"192.168.1.35","six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"3.2.1.0.8.a.0.c.f.f.f.f.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa","network":"::ffff:{expected_ipv4}","broadcast":"::ffff:{expected_ipv4}","hostmask":"::","netmask":"ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff","cidr_netmask":128,"hosts":1,"first_host":"::ffff:{expected_ipv4}","last_host":"::ffff:{expected_ipv4}","is_multicast":false,"is_private":true,"is_global":false,"is_link_local":false,"is_loopback":false,"is_reserved":{expected_is_reserved},"is_unspecified":false,"int":{{"ip":281473913979171,"network":281473913979171,"broadcast":281473913979171,"first_host":281473913979171,"last_host":281473913979171}},"hex":{{"ip":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","network":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","broadcast":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","hostmask":"00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00","netmask":"ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","first_host":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","last_host":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23"}},"bin":{{"ip":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","network":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","broadcast":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","hostmask":"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","netmask":"11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111","first_host":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","last_host":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011"}}}}''')

        try:
            self.assertEqual(actual, expected)
        except AssertionError:
            failures += 1
            failure_msgs.append(f'New-style IPv4 Mapped is_reserved=true failure:\n  Expected:  {expected}\n  Actual:  {actual}')

        # Old-Style IPv4 Mapped output with is_reserved=false
        expected_ipv4 = 'c0a8:123'
        expected_ipv4_exploded = 'c0a8:0123'
        expected_ipv4_split = '["0000", "0000", "0000", "0000", "0000", "ffff", "c0a8", "0123"]'
        expected_is_reserved = 'false'
        expected = json.loads(f'''{{"version":6,"max_prefix_length":128,"ip":"::ffff:{expected_ipv4}","ip_compressed":"::ffff:{expected_ipv4}","ip_exploded":"0000:0000:0000:0000:0000:ffff:{expected_ipv4_exploded}","ip_split":{expected_ipv4_split},"scope_id":null,"ipv4_mapped":"192.168.1.35","six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"3.2.1.0.8.a.0.c.f.f.f.f.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa","network":"::ffff:{expected_ipv4}","broadcast":"::ffff:{expected_ipv4}","hostmask":"::","netmask":"ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff","cidr_netmask":128,"hosts":1,"first_host":"::ffff:{expected_ipv4}","last_host":"::ffff:{expected_ipv4}","is_multicast":false,"is_private":true,"is_global":false,"is_link_local":false,"is_loopback":false,"is_reserved":{expected_is_reserved},"is_unspecified":false,"int":{{"ip":281473913979171,"network":281473913979171,"broadcast":281473913979171,"first_host":281473913979171,"last_host":281473913979171}},"hex":{{"ip":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","network":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","broadcast":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","hostmask":"00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00","netmask":"ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","first_host":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","last_host":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23"}},"bin":{{"ip":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","network":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","broadcast":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","hostmask":"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","netmask":"11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111","first_host":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","last_host":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011"}}}}''')

        try:
            self.assertEqual(actual, expected)
        except AssertionError:
            failures += 1
            failure_msgs.append(f'Old-style IPv4 Mapped is_reserved=false failure:\n  Expected:  {expected}\n  Actual:  {actual}')

        # Old-Style IPv4 Mapped output with is_reserved=true
        expected_is_reserved = 'true'
        expected = json.loads(f'''{{"version":6,"max_prefix_length":128,"ip":"::ffff:{expected_ipv4}","ip_compressed":"::ffff:{expected_ipv4}","ip_exploded":"0000:0000:0000:0000:0000:ffff:{expected_ipv4_exploded}","ip_split":{expected_ipv4_split},"scope_id":null,"ipv4_mapped":"192.168.1.35","six_to_four":null,"teredo_client":null,"teredo_server":null,"dns_ptr":"3.2.1.0.8.a.0.c.f.f.f.f.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa","network":"::ffff:{expected_ipv4}","broadcast":"::ffff:{expected_ipv4}","hostmask":"::","netmask":"ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff","cidr_netmask":128,"hosts":1,"first_host":"::ffff:{expected_ipv4}","last_host":"::ffff:{expected_ipv4}","is_multicast":false,"is_private":true,"is_global":false,"is_link_local":false,"is_loopback":false,"is_reserved":{expected_is_reserved},"is_unspecified":false,"int":{{"ip":281473913979171,"network":281473913979171,"broadcast":281473913979171,"first_host":281473913979171,"last_host":281473913979171}},"hex":{{"ip":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","network":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","broadcast":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","hostmask":"00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00","netmask":"ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","first_host":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23","last_host":"00:00:00:00:00:00:00:00:00:00:ff:ff:c0:a8:01:23"}},"bin":{{"ip":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","network":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","broadcast":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","hostmask":"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","netmask":"11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111","first_host":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011","last_host":"00000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111000000101010000000000100100011"}}}}''')

        try:
            self.assertEqual(actual, expected)
        except AssertionError:
            failures += 1
            failure_msgs.append(f'Old-style IPv4 Mapped is_reserved=true failure:\n  Expected:  {expected}\n  Actual:  {actual}')

        if failures > 3:
            self.fail('\n\n'.join(failure_msgs))


    def test_ip_address_ipv6_6to4(self):
        """
        Test ipv6 6to4 address string
        """
        # 6to4 behavior changes in newer versions of python are being backported
        # to old versions so we are checking if at least one style passes

        data = r'2002:c000:204::/48'
        actual = jc.parsers.ip_address.parse(data, quiet=True)
        failures = 0
        failure_msgs = []

        # New-Style 6to4 output
        expected_private = r'"is_private":true,"is_global":false'
        expected = json.loads(r'''{"version":6,"max_prefix_length":128,"ip":"2002:c000:204::","ip_compressed":"2002:c000:204::","ip_exploded":"2002:c000:0204:0000:0000:0000:0000:0000","ip_split":["2002","c000","0204","0000","0000","0000","0000","0000"],"scope_id":null,"ipv4_mapped":null,"six_to_four":"192.0.2.4","teredo_client":null,"teredo_server":null,"dns_ptr":"0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.4.0.2.0.0.0.0.c.2.0.0.2.ip6.arpa","network":"2002:c000:204::","broadcast":"2002:c000:204:ffff:ffff:ffff:ffff:ffff","hostmask":"::ffff:ffff:ffff:ffff:ffff","netmask":"ffff:ffff:ffff::","cidr_netmask":48,"hosts":1208925819614629174706174,"first_host":"2002:c000:204::1","last_host":"2002:c000:204:ffff:ffff:ffff:ffff:fffe","is_multicast":false,''' + expected_private + r''',"is_link_local":false,"is_loopback":false,"is_reserved":false,"is_unspecified":false,"int":{"ip":42549574682102084431821433448024768512,"network":42549574682102084431821433448024768512,"broadcast":42549574682103293357641048077199474687,"first_host":42549574682102084431821433448024768513,"last_host":42549574682103293357641048077199474686},"hex":{"ip":"20:02:c0:00:02:04:00:00:00:00:00:00:00:00:00:00","network":"20:02:c0:00:02:04:00:00:00:00:00:00:00:00:00:00","broadcast":"20:02:c0:00:02:04:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","hostmask":"00:00:00:00:00:00:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","netmask":"ff:ff:ff:ff:ff:ff:00:00:00:00:00:00:00:00:00:00","first_host":"20:02:c0:00:02:04:00:00:00:00:00:00:00:00:00:01","last_host":"20:02:c0:00:02:04:ff:ff:ff:ff:ff:ff:ff:ff:ff:fe"},"bin":{"ip":"00100000000000101100000000000000000000100000010000000000000000000000000000000000000000000000000000000000000000000000000000000000","network":"00100000000000101100000000000000000000100000010000000000000000000000000000000000000000000000000000000000000000000000000000000000","broadcast":"00100000000000101100000000000000000000100000010011111111111111111111111111111111111111111111111111111111111111111111111111111111","hostmask":"00000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111","netmask":"11111111111111111111111111111111111111111111111100000000000000000000000000000000000000000000000000000000000000000000000000000000","first_host":"00100000000000101100000000000000000000100000010000000000000000000000000000000000000000000000000000000000000000000000000000000001","last_host":"00100000000000101100000000000000000000100000010011111111111111111111111111111111111111111111111111111111111111111111111111111110"}}''')
        try:
            self.assertEqual(actual, expected)
        except AssertionError:
            failures += 1
            failure_msgs.append(f'New-style 6to4 address failure:\n  Expected:  {expected}\n  Actual:  {actual}')

        # Old-Style 6to4 output
        expected_private = r'"is_private":false,"is_global":true'
        expected = json.loads(r'''{"version":6,"max_prefix_length":128,"ip":"2002:c000:204::","ip_compressed":"2002:c000:204::","ip_exploded":"2002:c000:0204:0000:0000:0000:0000:0000","ip_split":["2002","c000","0204","0000","0000","0000","0000","0000"],"scope_id":null,"ipv4_mapped":null,"six_to_four":"192.0.2.4","teredo_client":null,"teredo_server":null,"dns_ptr":"0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.4.0.2.0.0.0.0.c.2.0.0.2.ip6.arpa","network":"2002:c000:204::","broadcast":"2002:c000:204:ffff:ffff:ffff:ffff:ffff","hostmask":"::ffff:ffff:ffff:ffff:ffff","netmask":"ffff:ffff:ffff::","cidr_netmask":48,"hosts":1208925819614629174706174,"first_host":"2002:c000:204::1","last_host":"2002:c000:204:ffff:ffff:ffff:ffff:fffe","is_multicast":false,''' + expected_private + r''',"is_link_local":false,"is_loopback":false,"is_reserved":false,"is_unspecified":false,"int":{"ip":42549574682102084431821433448024768512,"network":42549574682102084431821433448024768512,"broadcast":42549574682103293357641048077199474687,"first_host":42549574682102084431821433448024768513,"last_host":42549574682103293357641048077199474686},"hex":{"ip":"20:02:c0:00:02:04:00:00:00:00:00:00:00:00:00:00","network":"20:02:c0:00:02:04:00:00:00:00:00:00:00:00:00:00","broadcast":"20:02:c0:00:02:04:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","hostmask":"00:00:00:00:00:00:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","netmask":"ff:ff:ff:ff:ff:ff:00:00:00:00:00:00:00:00:00:00","first_host":"20:02:c0:00:02:04:00:00:00:00:00:00:00:00:00:01","last_host":"20:02:c0:00:02:04:ff:ff:ff:ff:ff:ff:ff:ff:ff:fe"},"bin":{"ip":"00100000000000101100000000000000000000100000010000000000000000000000000000000000000000000000000000000000000000000000000000000000","network":"00100000000000101100000000000000000000100000010000000000000000000000000000000000000000000000000000000000000000000000000000000000","broadcast":"00100000000000101100000000000000000000100000010011111111111111111111111111111111111111111111111111111111111111111111111111111111","hostmask":"00000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111","netmask":"11111111111111111111111111111111111111111111111100000000000000000000000000000000000000000000000000000000000000000000000000000000","first_host":"00100000000000101100000000000000000000100000010000000000000000000000000000000000000000000000000000000000000000000000000000000001","last_host":"00100000000000101100000000000000000000100000010011111111111111111111111111111111111111111111111111111111111111111111111111111110"}}''')
        try:
            self.assertEqual(actual, expected)
        except AssertionError:
            failures += 1
            failure_msgs.append(f'Old-style 6to4 address failure:\n  Expected:  {expected}\n  Actual:  {actual}')

        if failures > 1:
            self.fail('\n\n'.join(failure_msgs))


    def test_ip_address_ipv6_teredo(self):
        """
        Test ipv6 teredo address string
        """
        data = r'2001:0000:4136:e378:8000:63bf:3fff:fdd2'
        expected = json.loads(r'''{"version":6,"max_prefix_length":128,"ip":"2001:0:4136:e378:8000:63bf:3fff:fdd2","ip_compressed":"2001:0:4136:e378:8000:63bf:3fff:fdd2","ip_exploded":"2001:0000:4136:e378:8000:63bf:3fff:fdd2","ip_split":["2001","0000","4136","e378","8000","63bf","3fff","fdd2"],"scope_id":null,"ipv4_mapped":null,"six_to_four":null,"teredo_client":"192.0.2.45","teredo_server":"65.54.227.120","dns_ptr":"2.d.d.f.f.f.f.3.f.b.3.6.0.0.0.8.8.7.3.e.6.3.1.4.0.0.0.0.1.0.0.2.ip6.arpa","network":"2001:0:4136:e378:8000:63bf:3fff:fdd2","broadcast":"2001:0:4136:e378:8000:63bf:3fff:fdd2","hostmask":"::","netmask":"ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff","cidr_netmask":128,"hosts":1,"first_host":"2001:0:4136:e378:8000:63bf:3fff:fdd2","last_host":"2001:0:4136:e378:8000:63bf:3fff:fdd2","is_multicast":false,"is_private":true,"is_global":false,"is_link_local":false,"is_loopback":false,"is_reserved":false,"is_unspecified":false,"int":{"ip":42540488182158724593221357832373272018,"network":42540488182158724593221357832373272018,"broadcast":42540488182158724593221357832373272018,"first_host":42540488182158724593221357832373272018,"last_host":42540488182158724593221357832373272018},"hex":{"ip":"20:01:00:00:41:36:e3:78:80:00:63:bf:3f:ff:fd:d2","network":"20:01:00:00:41:36:e3:78:80:00:63:bf:3f:ff:fd:d2","broadcast":"20:01:00:00:41:36:e3:78:80:00:63:bf:3f:ff:fd:d2","hostmask":"00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00","netmask":"ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff","first_host":"20:01:00:00:41:36:e3:78:80:00:63:bf:3f:ff:fd:d2","last_host":"20:01:00:00:41:36:e3:78:80:00:63:bf:3f:ff:fd:d2"},"bin":{"ip":"00100000000000010000000000000000010000010011011011100011011110001000000000000000011000111011111100111111111111111111110111010010","network":"00100000000000010000000000000000010000010011011011100011011110001000000000000000011000111011111100111111111111111111110111010010","broadcast":"00100000000000010000000000000000010000010011011011100011011110001000000000000000011000111011111100111111111111111111110111010010","hostmask":"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","netmask":"11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111","first_host":"00100000000000010000000000000000010000010011011011100011011110001000000000000000011000111011111100111111111111111111110111010010","last_host":"00100000000000010000000000000000010000010011011011100011011110001000000000000000011000111011111100111111111111111111110111010010"}}''')
        self.assertEqual(jc.parsers.ip_address.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
