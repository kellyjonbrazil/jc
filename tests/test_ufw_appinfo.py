import os
import json
import unittest
import jc.parsers.ufw_appinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # new input/output fixtures
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-many-profiles.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_many_profiles = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-many-profiles.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_many_profiles_json = json.loads(f.read())

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ufw-appinfo-all.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_ufw_appinfo_all = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test2.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test2 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test3.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test3 = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-msn.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_msn = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-multiline-description.out'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_multiline_description = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ufw-appinfo-all.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_04_ufw_appinfo_all_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test2.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test2_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-test3.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_test3_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-msn.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_msn_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ufw-appinfo-multiline-description.json'), 'r', encoding='utf-8') as f:
        generic_ufw_appinfo_multiline_description_json = json.loads(f.read())


    def test_ufw_appinfo_line_separators(self):
        """
        Test 'ufw app info' with line-break characters other than LF in the title and description
        """
        data = 'Profile: TEST2\nTitle: My a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j app2\nDescription: a longer a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j.\n\nPorts:\n  53\n'
        result = jc.parsers.ufw_appinfo.parse(data, quiet=True)
        self.assertEqual(result[0]['title'], 'My a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j app2')
        self.assertEqual(result[0]['description'], 'a longer a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j.')
        self.assertEqual(result[0]['tcp_list'], [53])

    def test_ufw_appinfo_nodata(self):
        """
        Test 'ufw_appinfo' with no data
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse('', quiet=True), [])

    def test_ufw_appinfo_ubuntu_18_04_all(self):
        """
        Test 'ufw app info all' on Ubuntu 18.04
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.ubuntu_18_04_ufw_appinfo_all, quiet=True), self.ubuntu_18_04_ufw_appinfo_all_json)

    def test_ufw_appinfo_generic_test(self):
        """
        Test 'ufw app info [application]' sample
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_test, quiet=True), self.generic_ufw_appinfo_test_json)

    def test_ufw_appinfo_generic_test2(self):
        """
        Test 'ufw app info [application]' sample
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_test2, quiet=True), self.generic_ufw_appinfo_test2_json)

    def test_ufw_appinfo_generic_test3(self):
        """
        Test 'ufw app info [application]' sample
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_test3, quiet=True), self.generic_ufw_appinfo_test3_json)

    def test_ufw_appinfo_generic_msn(self):
        """
        Test 'ufw app info MSN' sample
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_msn, quiet=True), self.generic_ufw_appinfo_msn_json)

    def test_ufw_appinfo_generic_multiline_description(self):
        """
        Test 'ufw app info all' with mult-line description field
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_multiline_description, quiet=True), self.generic_ufw_appinfo_multiline_description_json)

    def test_ufw_appinfo_many_profiles(self):
        """
        Test 'ufw app info' with many profiles and wide port ranges
        """
        self.assertEqual(jc.parsers.ufw_appinfo.parse(self.generic_ufw_appinfo_many_profiles, quiet=True), self.generic_ufw_appinfo_many_profiles_json)

    def test_ufw_appinfo_normalized_ports(self):
        """
        Test 'ufw app info' normalized ports: merged and adjacent ranges,
        listed ports inside ranges, and a very large range
        """
        data = 'Profile: T\nTitle: t\nDescription: d\n\nPorts:\n  1:5,6:10,20,30:40,35:50,12,45/tcp\n  1:100000000/udp\n'
        result = jc.parsers.ufw_appinfo.parse(data, quiet=True)[0]
        self.assertEqual(result['normalized_tcp_ranges'], [{'start': 1, 'end': 10}, {'start': 30, 'end': 50}])
        self.assertEqual(result['normalized_tcp_list'], [12, 20])
        self.assertNotIn('normalized_udp_ranges', result)

    def test_ufw_appinfo_whitespace_line_and_repeated_protocol(self):
        """
        Test 'ufw_appinfo' with a whitespace-only line, repeated protocol lines and a token containing 'any'
        """
        data = (
            'Profile: App\n'
            'Title: App\n'
            'Description: App\n'
            '\n'
            'Ports:\n'
            '  80/tcp\n'
            '   \n'
            '  443,8000:8010/tcp\n'
            '  53/udp\n'
            '  67,/udp\n'
            '  70/udp\n'
        )
        result = jc.parsers.ufw_appinfo.parse(data, quiet=True)
        self.assertEqual(result[0]['tcp_list'], [80, 443])
        self.assertEqual(result[0]['tcp_ranges'], [{'start': 8000, 'end': 8010}])
        self.assertEqual(result[0]['udp_list'], [53, 67, 70])

        # a token that only contains 'any' is not the 'any' keyword
        raw_result = jc.parsers.ufw_appinfo.parse(data.replace('67,', 'many,'), raw=True, quiet=True)
        self.assertEqual(raw_result[0]['udp_list'], ['53', 'many', '70'])


if __name__ == '__main__':
    unittest.main()
