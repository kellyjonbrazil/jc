import os
import json
import unittest
import jc.parsers.ss

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ss-sudo-a.out'), 'r', encoding='utf-8') as f:
        centos_7_7_ss_sudo_a = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ss-sudo-a.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ss_sudo_a = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ss-sudo-tulpen.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ss_sudo_tulpen = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-wide.out'), 'r', encoding='utf-8') as f:
        ss_wide = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian-12/ss-sudo-tulnpe.out'), 'r', encoding='utf-8') as f:
        debian_12_ss_sudo_tulnpe = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-users-edge-cases.out'), 'r', encoding='utf-8') as f:
        ss_users_edge_cases = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/ss-sudo-a.json'), 'r', encoding='utf-8') as f:
        centos_7_7_ss_sudo_a_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ss-sudo-a.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ss_sudo_a_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/ss-sudo-tulpen.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_ss_sudo_tulpen_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-wide.json'), 'r', encoding='utf-8') as f:
        ss_wide_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/debian-12/ss-sudo-tulnpe.json'), 'r', encoding='utf-8') as f:
        debian_12_ss_sudo_tulnpe_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-users-edge-cases.json'), 'r', encoding='utf-8') as f:
        ss_users_edge_cases_json = json.loads(f.read())

    def test_ss_nodata(self):
        """
        Test 'ss' with no data
        """
        self.assertEqual(jc.parsers.ss.parse('', quiet=True), [])

    def test_ss_sudo_a_centos_7_7(self):
        """
        Test 'sudo ss -a' on Centos 7.7
        """
        self.assertEqual(jc.parsers.ss.parse(self.centos_7_7_ss_sudo_a, quiet=True), self.centos_7_7_ss_sudo_a_json)

    def test_ss_sudo_a_ubuntu_18_4(self):
        """
        Test 'sudo ss -a' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ss.parse(self.ubuntu_18_4_ss_sudo_a, quiet=True), self.ubuntu_18_4_ss_sudo_a_json)

    def test_ss_sudo_tulpen_ubuntu_18_4(self):
        """
        Test 'sudo ss -tulpen' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.ss.parse(self.ubuntu_18_4_ss_sudo_tulpen, quiet=True), self.ubuntu_18_4_ss_sudo_tulpen_json)

    def test_ss_wide(self):
        """
        Test 'sudo ss' with wide format and lots of options
        """
        self.assertEqual(jc.parsers.ss.parse(self.ss_wide, quiet=True), self.ss_wide_json)

    def test_ss_sudo_tulnpe_debian_12(self):
        """
        Test 'sudo ss -tulnpe' on Debian 12 with awkward process names

        Three listeners whose command names exercise the users: parsing:
        one plain, one containing a space and a colon, and one containing a
        parenthesis. Before the fix the space/colon name raised SyntaxError
        from ast.literal_eval and the parenthesis was silently rewritten to a
        bracket, so 'svc(1' was reported as 'svc[1'.
        """
        self.assertEqual(jc.parsers.ss.parse(self.debian_12_ss_sudo_tulnpe, quiet=True), self.debian_12_ss_sudo_tulnpe_json)

    def test_ss_users_edge_cases(self):
        """
        Test 'ss' users: parsing edge cases beyond the debian-12 fixture:

        - a process name that is itself wrapped in parens ('(sd-pam)', a
          real systemd user-session process name)
        - two users: records sharing one users:() block, both containing a
          space and a colon ('nginx: worker process', a real nginx name)
        - users: combined with timer: in the same opts field, and a process
          name containing balanced parens ('app(prod)')
        """
        self.assertEqual(jc.parsers.ss.parse(self.ss_users_edge_cases, quiet=True), self.ss_users_edge_cases_json)


if __name__ == '__main__':
    unittest.main()
