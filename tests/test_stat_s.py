import os
import json
import unittest
from jc.exceptions import ParseError
import jc.parsers.stat_s

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# To create streaming output use:
# $ cat stat.out | jc --stat-s | jello -c > stat-streaming.json


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/stat.out'), 'r', encoding='utf-8') as f:
        centos_7_7_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/stat.out'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/stat.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_stat = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/stat-filename-with-spaces.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_stat_filename_with_spaces = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/stat.out'), 'r', encoding='utf-8') as f:
        freebsd12_stat = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/stat-streaming.json'), 'r', encoding='utf-8') as f:
        centos_7_7_stat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/stat-streaming.json'), 'r', encoding='utf-8') as f:
        ubuntu_18_4_stat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/stat-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_stat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/stat-filename-with-spaces-streaming.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_stat_filename_with_spaces_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/freebsd12/stat-streaming.json'), 'r', encoding='utf-8') as f:
        freebsd12_stat_streaming_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/stat-linux-arrows.out'), 'r', encoding='utf-8') as f:
        generic_stat_linux_arrows = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/stat-linux-arrows-streaming.json'), 'r', encoding='utf-8') as f:
        generic_stat_linux_arrows_streaming_json = json.loads(f.read())

    def test_stat_s_nodata(self):
        """
        Test 'stat' with no data
        """
        self.assertEqual(list(jc.parsers.stat_s.parse([], quiet=True)), [])

    def test_stat_s_unparsable(self):
        data = 'unparsable data'
        g = jc.parsers.stat_s.parse(data.splitlines(), quiet=True)
        with self.assertRaises(ParseError):
            list(g)

    def test_stat_s_centos_7_7(self):
        """
        Test 'stat /bin/*' on Centos 7.7
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.centos_7_7_stat.splitlines(), quiet=True)), self.centos_7_7_stat_streaming_json)

    def test_stat_s_ubuntu_18_4(self):
        """
        Test 'stat /bin/*' on Ubuntu 18.4
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.ubuntu_18_4_stat.splitlines(), quiet=True)), self.ubuntu_18_4_stat_streaming_json)

    def test_stat_s_osx_10_14_6(self):
        """
        Test 'stat /bin/*' on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.osx_10_14_6_stat.splitlines(), quiet=True)), self.osx_10_14_6_stat_streaming_json)

    def test_stat_s_filename_with_spaces_osx_10_14_6(self):
        """
        Test 'stat' filename with spaces on OSX 10.14.6
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.osx_10_14_6_stat_filename_with_spaces.splitlines(), quiet=True)), self.osx_10_14_6_stat_filename_with_spaces_streaming_json)

    def test_stat_s_freebsd12(self):
        """
        Test 'stat /foo/*' on FreeBSD12
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.freebsd12_stat.splitlines(), quiet=True)), self.freebsd12_stat_streaming_json)

    def test_stat_s_arrows(self):
        """
        Test 'stat' with ' -> ' in the names of files, directories, and symbolic links
        """
        self.assertEqual(list(jc.parsers.stat_s.parse(self.generic_stat_linux_arrows.splitlines(), quiet=True)), self.generic_stat_linux_arrows_streaming_json)

    def test_stat_s_arrows_link_to(self):
        """
        Test that only symbolic links get link_to, split at the first ' -> '
        """
        result = list(jc.parsers.stat_s.parse(self.generic_stat_linux_arrows.splitlines(), raw=True, quiet=True))
        self.assertEqual([(r['file'], r.get('link_to')) for r in result], [('arrowtarget', 'a -> b'), ('deploy.key', None), ('deploy.key -> old', None), ('dir -> y', None), ('lnk', 'x -> target'), ('normallnk', 'tgt')])
        self.assertEqual(result[2]['type'], 'regular empty file')

    def test_stat_s_link_quoted(self):
        """
        Test a symbolic link in the quoted format of older 'stat' versions
        """
        data = '  File: \u2018lnk\u2019 -> \u2018a -> b\u2019\n  Size: 6         \tBlocks: 0          IO Block: 4096   symbolic link\n'
        result = list(jc.parsers.stat_s.parse(data.splitlines(), raw=True, quiet=True))
        self.assertEqual(result, [{'file': 'lnk', 'link_to': 'a -> b', 'size': '6', 'blocks': '0', 'io_blocks': '4096', 'type': 'symbolic link'}])


    def test_stat_s_bsd_apostrophe(self):
        """
        Test 'stat' on macOS/FreeBSD with an apostrophe and a quote in the file names
        """
        pre = '16777220 161929661 -rw-r--r-- 1 kbrazil staff 0 5 "Aug 13 15:03:52 2021" "Aug 13 14:37:03 2021" "Aug 13 14:37:03 2021" "Aug 13 14:37:03 2021" 4096 8 0 '
        data = [pre + "it's here.txt\n", pre + 'say "hi" \\ x.txt\n', pre + 'a  b.txt\n']
        result = list(jc.parsers.stat_s.parse(data, raw=True, quiet=True))
        self.assertEqual([r['file'] for r in result], ["it's here.txt", 'say "hi" \\ x.txt', 'a  b.txt'])
        self.assertEqual(result[0]['access_time'], 'Aug 13 15:03:52 2021')
        self.assertEqual(result[0]['unix_flags'], '0')

    def test_stat_s_linux_whitespace_file_name(self):
        """
        Test 'stat' on Linux with a file name that is only whitespace
        """
        rest = ('  Size: 0         \tBlocks: 0          IO Block: 4096   regular empty file\n'
                'Device: 801h/2049d\tInode: 12          Links: 1\n'
                'Access: (0644/-rw-r--r--)  Uid: ( 1000/    user)   Gid: ( 1000/    user)\n'
                'Access: 2021-08-13 15:03:52.000000000 -0700\n'
                'Modify: 2021-08-13 15:03:52.000000000 -0700\n'
                'Change: 2021-08-13 15:03:52.000000000 -0700\n'
                ' Birth: -\n')
        data = ("  File: '   '\n" + rest + '  File:    \n' + rest + '  File: ok\n' + rest).splitlines(True)
        result = list(jc.parsers.stat_s.parse(data, raw=True, quiet=True))
        self.assertEqual([r['file'] for r in result], ["'   '", '   ', 'ok'])
        self.assertEqual([r['inode'] for r in result], ['12', '12', '12'])


if __name__ == '__main__':
    unittest.main()
