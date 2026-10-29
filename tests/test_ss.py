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

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-service-port-names.out'), 'r', encoding='utf-8') as f:
        generic_ss_service_port_names = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-service-port-names.json'), 'r', encoding='utf-8') as f:
        generic_ss_service_port_names_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-port-process-header.out'), 'r', encoding='utf-8') as f:
        generic_ss_port_process_header = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-port-process-header.json'), 'r', encoding='utf-8') as f:
        generic_ss_port_process_header_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-linux-unix-name-spaces.out'), 'r', encoding='utf-8') as f:
        generic_ss_linux_unix_name_spaces = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-linux-unix-name-spaces.json'), 'r', encoding='utf-8') as f:
        generic_ss_linux_unix_name_spaces_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-linux-full-columns.out'), 'r', encoding='utf-8') as f:
        generic_ss_linux_full_columns = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-linux-full-columns.json'), 'r', encoding='utf-8') as f:
        generic_ss_linux_full_columns_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-linux-detail-lines.out'), 'r', encoding='utf-8') as f:
        generic_ss_linux_detail_lines = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/ss-linux-detail-lines.json'), 'r', encoding='utf-8') as f:
        generic_ss_linux_detail_lines_json = json.loads(f.read())

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

    def test_ss_service_port_names(self):
        """
        Test 'ss' with service names that contain digits as ports
        """
        self.assertEqual(jc.parsers.ss.parse(self.generic_ss_service_port_names, quiet=True), self.generic_ss_service_port_names_json)

    def test_ss_port_process_header(self):
        """
        Test 'ss' with a 'Port Process' header written with a space
        """
        self.assertEqual(jc.parsers.ss.parse(self.generic_ss_port_process_header, quiet=True), self.generic_ss_port_process_header_json)


    def test_ss_unix_name_spaces(self):
        """
        Test 'ss -a' with netlink and unix socket names that contain spaces
        before ordinary unix socket rows
        """
        self.assertEqual(jc.parsers.ss.parse(self.generic_ss_linux_unix_name_spaces, quiet=True), self.generic_ss_linux_unix_name_spaces_json)

    def test_ss_unix_name_spaces_unaligned(self):
        """
        Test 'ss -a' on Centos 7.7 with an added unix socket row whose name
        contains a space: the other records do not change
        """
        lines = self.centos_7_7_ss_sudo_a.splitlines()
        first_unix = next(i for i, line in enumerate(lines) if line.startswith('u_'))
        lines.insert(first_unix, 'u_str  LISTEN     0      128    /tmp/a b 99999                  * 0')
        result = jc.parsers.ss.parse('\n'.join(lines), quiet=True)
        added = result.pop(first_unix - 1)
        self.assertEqual(result, self.centos_7_7_ss_sudo_a_json)
        self.assertEqual((added['path'], added['local_port'], added['peer_address'], added['peer_port']),
                         ('/tmp/a b', '99999', '*', '0'))

    def test_ss_full_columns(self):
        """
        Test 'ss -tuxpe' rows where a full Recv-Q or Port column leaves only
        one space before the next column
        """
        self.assertEqual(jc.parsers.ss.parse(self.generic_ss_linux_full_columns, quiet=True), self.generic_ss_linux_full_columns_json)

    def test_ss_timer_empty_time(self):
        """
        Test 'ss -o' with a timer whose expire time is empty
        """
        data = ('Netid State Recv-Q Send-Q Local Address:Port Peer Address:Port Process\n'
                'tcp   ESTAB 0      0         10.0.0.5:22       10.0.0.9:40000 timer:(keepalive,,0) ino:5 sk:5 <->')
        opts = jc.parsers.ss.parse(data, quiet=True)[0]['opts']
        self.assertEqual(opts['timer'], {'timer_name': 'keepalive', 'expire_time': '', 'retrans': '0'})


    def test_ss_netlink_name_with_space(self):
        """
        Test 'ss' netlink rows whose process name has spaces and slashes
        """
        data = ('Netid State  Recv-Q Send-Q        Local Address:Port  Peer Address:Port\n'
                'nl    UNCONN 0      0           rtnl:my proc/123                  *\n'
                'nl    UNCONN 0      0           rtnl:kernel                       *\n'
                'nl    UNCONN 0      0           rtnl:a/b c/1 x/77                 *\n'
                'nl    UNCONN 0      0           rtnl:x  y/5                       *\n'
                'nl    UNCONN 0      0           rtnl:systemd/1                    *\n')
        result = jc.parsers.ss.parse(data, quiet=True)
        self.assertEqual([(r['channel'], r.get('pid'), r['peer_address'], r.get('peer_port')) for r in result], [
            ('rtnl:my proc', 123, '*', None),
            ('rtnl:kernel', None, '*', None),
            ('rtnl:a/b c/1 x', 77, '*', None),
            ('rtnl:x  y', 5, '*', None),
            ('rtnl:systemd', 1, '*', None)
        ])

    def test_ss_unix_percent_in_path(self):
        """
        Test 'ss' unix socket paths with a '%' that is not an interface
        """
        data = ('Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port\n'
                'u_str LISTEN 0      4096   @foo%bar 1234       * 0\n'
                'u_str LISTEN 0      4096   /run/a%b 1235       * 0\n'
                'udp   UNCONN 0      0      127.0.0.53%lo:53    0.0.0.0:*\n')
        result = jc.parsers.ss.parse(data, quiet=True)
        self.assertEqual(result[0]['path'], '@foo%bar')
        self.assertNotIn('interface', result[0])
        self.assertEqual(result[1]['path'], '/run/a%b')
        self.assertNotIn('interface', result[1])
        self.assertEqual((result[2]['local_address'], result[2]['interface']), ('127.0.0.53', 'lo'))

    def test_ss_packet_sockets(self):
        """
        Test 'ss -0' and 'ss -0e' with p_raw and p_dgr rows
        """
        data = ('Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process\n'
                'p_raw UNCONN 0      0               LLDP:ens33                  *        ino:30371 sk:1 cgroup:/system.slice/lldpd.service <->\n'
                'p_dgr UNCONN 0      0            [35020]:wlp2s0                 *        ino:28737 sk:2 cgroup:/system.slice/NetworkManager.service <->\n'
                'p_dgr UNCONN 0      0                 ip:*                      *        ino:28738 sk:3 cgroup:/ <->\n')
        result = jc.parsers.ss.parse(data, quiet=True)
        self.assertEqual(result, [
            {'netid': 'p_raw', 'state': 'UNCONN', 'recv_q': 0, 'send_q': 0, 'peer_address': '*',
             'opts': {'inode_number': '30371', 'cookie': '1', 'cgroup': '/system.slice/lldpd.service'},
             'link_layer': 'LLDP', 'interface': 'ens33'},
            {'netid': 'p_dgr', 'state': 'UNCONN', 'recv_q': 0, 'send_q': 0, 'peer_address': '*',
             'opts': {'inode_number': '28737', 'cookie': '2', 'cgroup': '/system.slice/NetworkManager.service'},
             'link_layer': '[35020]', 'interface': 'wlp2s0'},
            {'netid': 'p_dgr', 'state': 'UNCONN', 'recv_q': 0, 'send_q': 0, 'peer_address': '*',
             'opts': {'inode_number': '28738', 'cookie': '3', 'cgroup': '/'},
             'link_layer': 'ip', 'interface': '*'}
        ])

        data = ('Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process\n'
                'p_dgr UNCONN 0      0            [35020]:wlp2s0                 *\n')
        result = jc.parsers.ss.parse(data, quiet=True)
        self.assertEqual(result, [
            {'netid': 'p_dgr', 'state': 'UNCONN', 'recv_q': 0, 'send_q': 0, 'peer_address': '*',
             'link_layer': '[35020]', 'interface': 'wlp2s0'}
        ])

    def test_ss_users_with_contexts_and_threads(self):
        """
        Test 'ss -pZ', 'ss -pz' and 'ss -pT' process records
        """
        data = ('Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process\n'
                'tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=1023,proc_ctx=system_u:system_r:sshd_t:s0-s0:c0.c1023,fd=3))\n'
                'tcp   LISTEN 0      128          0.0.0.0:23         0.0.0.0:*    users:(("a b",pid=5,proc_ctx=u:r:t:s0:c1,c5,fd=4,sock_ctx=u:r:t:s0),("a b",pid=6,tid=7,fd=8))\n')
        result = jc.parsers.ss.parse(data, quiet=True)
        self.assertEqual(result[0]['opts'], {'process_id': {'1023': {'user': 'sshd', 'file_descriptor': '3'}}})
        self.assertEqual(result[0]['local_port'], '22')
        self.assertEqual(result[1]['opts'], {'process_id': {
            '5': {'user': 'a b', 'file_descriptor': '4'},
            '6': {'user': 'a b', 'file_descriptor': '8'}
        }})

    def test_ss_linux_detail_lines(self):
        """
        Test 'ss -a -e -i -m' where indented detail lines follow each socket row
        """
        self.assertEqual(jc.parsers.ss.parse(self.generic_ss_linux_detail_lines, quiet=True), self.generic_ss_linux_detail_lines_json)

    def test_ss_linux_detail_lines_not_records(self):
        """
        Test 'ss' gives one record per socket row and ignores the indented detail lines
        """
        rows = jc.parsers.ss.parse(self.generic_ss_linux_detail_lines, quiet=True)
        self.assertEqual([r['netid'] for r in rows], ['p_dgr', 'p_dgr', 'icmp6', 'udp', 'udp', 'tcp', 'tcp'])
        self.assertEqual(rows[1]['interface'], '*')
        self.assertNotIn('peer_port', rows[1])


if __name__ == '__main__':
    unittest.main()
