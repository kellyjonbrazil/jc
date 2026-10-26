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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-padded-opts.out'), 'r', encoding='utf-8') as f:
        ss_padded_opts = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-users-unclosed.out'), 'r', encoding='utf-8') as f:
        ss_users_unclosed = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-cgroup-spaces.out'), 'r', encoding='utf-8') as f:
        ss_cgroup_spaces = f.read()

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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-padded-opts.json'), 'r', encoding='utf-8') as f:
        ss_padded_opts_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-users-unclosed.json'), 'r', encoding='utf-8') as f:
        ss_users_unclosed_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-cgroup-spaces.json'), 'r', encoding='utf-8') as f:
        ss_cgroup_spaces_json = json.loads(f.read())

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

    def test_ss_padded_opts(self):
        """
        Test 'ss' where the options region itself contains runs of two or more
        spaces, which newer iproute2 emits to align the users: column.

        The first two rows are the same socket with one space and with five;
        they must parse identically apart from ino and sk.
        """
        self.assertEqual(jc.parsers.ss.parse(self.ss_padded_opts, quiet=True), self.ss_padded_opts_json)

    def test_ss_padded_opts_matches_unpadded(self):
        """
        Padding is alignment, not data: widening the gap before ino: must not
        change how the row is parsed.
        """
        rows = jc.parsers.ss.parse(self.ss_padded_opts, quiet=True)
        unpadded, padded = rows[0]['opts'], rows[1]['opts']
        self.assertEqual(unpadded['process_id']['3241']['user'],
                         padded['process_id']['3242']['user'])
        self.assertEqual(unpadded['cgroup'], padded['cgroup'])
        self.assertEqual(sorted(unpadded), sorted(padded))

    def test_ss_users_unclosed(self):
        """
        Test 'ss' rows whose users: block is never closed, or holds a long
        run of '("' after its last complete record
        """
        self.assertEqual(jc.parsers.ss.parse(self.ss_users_unclosed, quiet=True), self.ss_users_unclosed_json)

    def test_ss_users_records(self):
        """
        Test 'ss' users: records: several records in one block, names that
        contain '("' or 'users:((', and a block that is only closed by '))'
        followed by a space or the end of the row
        """
        header = 'Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess\n'
        row = 'tcp   LISTEN 0      5            0.0.0.0:19001      0.0.0.0:*    '
        cases = {
            'users:(("a",pid=1,fd=2),("b",pid=3,fd=4))':
                {'1': {'user': 'a', 'file_descriptor': '2'},
                 '3': {'user': 'b', 'file_descriptor': '4'}},
            'users:(("("x",pid=7,fd=8),("users:((",pid=9,fd=10))':
                {'7': {'user': '("x', 'file_descriptor': '8'},
                 '9': {'user': 'users:((', 'file_descriptor': '10'}},
            'users:(("a))b",pid=11,fd=12)) ino:1':
                {'11': {'user': 'a))b', 'file_descriptor': '12'}}
        }

        for users, expected in cases.items():
            with self.subTest(users):
                opts = jc.parsers.ss.parse(header + row + users + '\n', quiet=True)[0]['opts']
                self.assertEqual(opts['process_id'], expected)


    def test_ss_cgroup_spaces(self):
        """
        Test 'ss -tulnpe' with cgroup paths that contain spaces and text in
        the form of other fields
        """
        self.assertEqual(jc.parsers.ss.parse(self.ss_cgroup_spaces, quiet=True), self.ss_cgroup_spaces_json)

    def test_ss_cgroup_fields_in_path(self):
        """
        Test 'ss -e' where the cgroup path contains uid:, ino: and users:
        text. The values ss printed for the socket are kept.
        """
        rows = jc.parsers.ss.parse(self.ss_cgroup_spaces, quiet=True)

        opts = rows[3]['opts']
        self.assertEqual(opts['uid_number'], '1000')
        self.assertEqual(opts['inode_number'], '2415307')
        self.assertEqual(opts['cgroup'], '/user.slice/user-1000.slice/user@1000.service/app.slice/my app uid:0 ino:30488 cgroup:/system.slice/ssh.service')

        opts = rows[4]['opts']
        self.assertNotIn('process_id', opts)
        self.assertEqual(opts['inode_number'], '2415308')
        self.assertEqual(opts['cgroup'], '/user.slice/user-1000.slice/user@1000.service/app.slice/web users:(("sshd",pid=1161,fd=3)) timer:x')

        # the key renames do not change the path
        self.assertEqual(rows[1]['opts']['cgroup'], '/system.slice/squid.service')

    def test_ss_cgroup_trailing_tokens(self):
        """
        Test 'ss -e' with the tokens printed after the cgroup path: v6only,
        fwmark, the shutdown markers, and the one-line (-O) fields after the
        marker
        """
        header = 'Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess\n'
        row = 'tcp   LISTEN 0      5               [::]:19003         [::]:*    uid:1000 ino:5 sk:a006 '
        cases = {
            'cgroup:/a b <->': {'cgroup': '/a b'},
            'cgroup:/a b -->': {'cgroup': '/a b'},
            'cgroup:/a b <--': {'cgroup': '/a b'},
            'cgroup:/a b ---': {'cgroup': '/a b'},
            'cgroup:/a b v6only:1 <->': {'cgroup': '/a b', 'v6only': '1'},
            'cgroup:/a b fwmark:0x1f v6only:0 <->': {'cgroup': '/a b', 'fwmark': '0x1f', 'v6only': '0'},
            'cgroup:/a <-> uid:0 <->': {'cgroup': '/a <-> uid:0'},
            'cgroup:/a <-> uid:0': {'cgroup': '/a <-> uid:0'},
            'cgroup:/a b <-> skmem:(r0,rb131072) ts sack cubic wscale:7,7':
                {'cgroup': '/a b', 'skmem': '(r0,rb131072)', 'wscale': '7,7'}
        }

        for opts_text, expected in cases.items():
            with self.subTest(opts_text):
                opts = jc.parsers.ss.parse(header + row + opts_text + '\n', quiet=True)[0]['opts']
                expected.update({'uid_number': '1000', 'inode_number': '5', 'cookie': 'a006'})
                self.assertEqual(opts, expected)


if __name__ == '__main__':
    unittest.main()
