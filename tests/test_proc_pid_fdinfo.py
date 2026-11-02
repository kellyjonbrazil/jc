import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_pid_fdinfo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_pid_fdinfo': (
                'fixtures/linux-proc/pid_fdinfo',
                'fixtures/linux-proc/pid_fdinfo.json'),
            'proc_pid_fdinfo_dma': (
                'fixtures/linux-proc/pid_fdinfo_dma',
                'fixtures/linux-proc/pid_fdinfo_dma.json'),
            'proc_pid_fdinfo_epoll': (
                'fixtures/linux-proc/pid_fdinfo_epoll',
                'fixtures/linux-proc/pid_fdinfo_epoll.json'),
            'proc_pid_fdinfo_fanotify': (
                'fixtures/linux-proc/pid_fdinfo_fanotify',
                'fixtures/linux-proc/pid_fdinfo_fanotify.json'),
            'proc_pid_fdinfo_inotify': (
                'fixtures/linux-proc/pid_fdinfo_inotify',
                'fixtures/linux-proc/pid_fdinfo_inotify.json'),
            'proc_pid_fdinfo_timerfd': (
                'fixtures/linux-proc/pid_fdinfo_timerfd',
                'fixtures/linux-proc/pid_fdinfo_timerfd.json'),
            'proc_pid_fdinfo_long_epoll': (
                'fixtures/generic/proc-pid-fdinfo-long-epoll.out',
                'fixtures/generic/proc-pid-fdinfo-long-epoll.json'),
            'proc_pid_fdinfo_epoll_multi': (
                'fixtures/linux-proc/pid_fdinfo_epoll_multi',
                'fixtures/linux-proc/pid_fdinfo_epoll_multi.json'),
            'proc_pid_fdinfo_inotify_multi': (
                'fixtures/linux-proc/pid_fdinfo_inotify_multi',
                'fixtures/linux-proc/pid_fdinfo_inotify_multi.json'),
            'proc_pid_fdinfo_lock_multi': (
                'fixtures/linux-proc/pid_fdinfo_lock_multi',
                'fixtures/linux-proc/pid_fdinfo_lock_multi.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_pid_fdinfo_nodata(self):
        """
        Test 'proc_pid_fdinfo' with no data
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse('', quiet=True), {})

    def test_proc_pid_fdinfo(self):
        """
        Test '/proc/<pid>/fdinfo/<fd>'
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(self.f_in['proc_pid_fdinfo'], quiet=True),
                                                          self.f_json['proc_pid_fdinfo'])

    def test_proc_pid_fdinfo_dma(self):
        """
        Test '/proc/<pid>/fdinfo/<fd>' dma file
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(self.f_in['proc_pid_fdinfo_dma'], quiet=True),
                                                          self.f_json['proc_pid_fdinfo_dma'])

    def test_proc_pid_fdinfo_epoll(self):
        """
        Test '/proc/<pid>/fdinfo/<fd>' epoll file
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(self.f_in['proc_pid_fdinfo_epoll'], quiet=True),
                                                          self.f_json['proc_pid_fdinfo_epoll'])

    def test_proc_pid_fdinfo_fanotify(self):
        """
        Test '/proc/<pid>/fdinfo/<fd>' fanotify file
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(self.f_in['proc_pid_fdinfo_fanotify'], quiet=True),
                                                          self.f_json['proc_pid_fdinfo_fanotify'])

    def test_proc_pid_fdinfo_inotify(self):
        """
        Test '/proc/<pid>/fdinfo/<fd>' inotify file
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(self.f_in['proc_pid_fdinfo_inotify'], quiet=True),
                                                          self.f_json['proc_pid_fdinfo_inotify'])

    def test_proc_pid_fdinfo_timerfd(self):
        """
        Test '/proc/<pid>/fdinfo/<fd>' timerfd file
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(self.f_in['proc_pid_fdinfo_timerfd'], quiet=True),
                                                          self.f_json['proc_pid_fdinfo_timerfd'])

    def test_proc_pid_fdinfo_long_epoll(self):
        """
        Test '/proc/<pid>/fdinfo/<fd>' epoll file with a long word in the tfd line
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(self.f_in['proc_pid_fdinfo_long_epoll'], quiet=True),
                                                          self.f_json['proc_pid_fdinfo_long_epoll'])


    def test_proc_pid_fdinfo_line_separator(self):
        """
        Test 'proc_pid_fdinfo' with a line-break character other than LF inside a field
        """
        data = 'pos:\t0\nflags:\t02000002\nmnt_id:\t15\nino:\t19946\nUserFiles:\t1\n    0: r\x0cino:1\x0cmnt_id:1\x0cpos:7\nUserBufs:\t0\n'
        result = jc.parsers.proc_pid_fdinfo.parse(data, quiet=True)
        self.assertEqual((result['pos'], result['mnt_id'], result['ino']), (0, 15, 19946))
        self.assertEqual(result['0'], 'r\x0cino:1\x0cmnt_id:1\x0cpos:7')


    def test_proc_pid_fdinfo_octal_flags(self):
        """
        Test 'proc_pid_fdinfo' with octal open flags
        """
        data = 'pos:\t0\nflags:\t02100000\nmnt_id:\t44\nino:\t9658574\n'
        expected = {'pos': 0, 'flags': 557056, 'mnt_id': 44, 'ino': 9658574}
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(data, quiet=True), expected)

    def test_proc_pid_fdinfo_inotify_hex_wd(self):
        """
        Test 'proc_pid_fdinfo' with hexadecimal inotify watch descriptors
        """
        data = 'pos:\t0\nflags:\t02004000\nmnt_id:\t19\nino:\t84\ninotify wd:1a ino:9360d7 sdev:fc00000 mask:2 ignored_mask:0 fhandle-bytes:c fhandle-type:81 f_handle:d7609300000000005bcd4b8d\n'
        result = jc.parsers.proc_pid_fdinfo.parse(data, quiet=True)
        self.assertEqual((result['flags'], result['inotify'][0]['wd'], result['inotify'][0]['ino']), (526336, 26, '9360d7'))

        data = data.replace('wd:1a', 'wd:a')
        result = jc.parsers.proc_pid_fdinfo.parse(data, quiet=True)
        self.assertEqual((result['inotify'][0]['wd'], result['inotify'][0]['ino']), (10, '9360d7'))


    def test_proc_pid_fdinfo_epoll_multi(self):
        """
        Test '/proc/<pid>/fdinfo/<fd>' epoll file with two targets
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(self.f_in['proc_pid_fdinfo_epoll_multi'], quiet=True),
                                                          self.f_json['proc_pid_fdinfo_epoll_multi'])

    def test_proc_pid_fdinfo_inotify_multi(self):
        """
        Test '/proc/<pid>/fdinfo/<fd>' inotify file with three watches
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(self.f_in['proc_pid_fdinfo_inotify_multi'], quiet=True),
                                                          self.f_json['proc_pid_fdinfo_inotify_multi'])

    def test_proc_pid_fdinfo_lock_multi(self):
        """
        Test '/proc/<pid>/fdinfo/<fd>' file with two locks
        """
        self.assertEqual(jc.parsers.proc_pid_fdinfo.parse(self.f_in['proc_pid_fdinfo_lock_multi'], quiet=True),
                                                          self.f_json['proc_pid_fdinfo_lock_multi'])

    def test_proc_pid_fdinfo_fanotify_marks(self):
        """
        Test 'proc_pid_fdinfo' fanotify file with no marks and with superblock and mount namespace marks
        """
        data = 'pos:\t0\nflags:\t02\nmnt_id:\t9\nino:\t63107\nfanotify flags:10 event-flags:0\n'
        result = jc.parsers.proc_pid_fdinfo.parse(data, quiet=True)
        self.assertEqual(result['fanotify'], {'flags': '10', 'event-flags': '0', 'marks': []})

        data += 'fanotify sdev:800013 mflags:0 mask:3b ignored_mask:0\nfanotify mnt_ns:4026531841 mflags:0 mask:1000000 ignored_mask:0\n'
        expected = {
            'flags': '10',
            'event-flags': '0',
            'marks': [
                {'sdev': '800013', 'mflags': '0', 'mask': '3b', 'ignored_mask': '0'},
                {'mnt_ns': '4026531841', 'mflags': '0', 'mask': '1000000', 'ignored_mask': '0'}
            ]
        }
        result = jc.parsers.proc_pid_fdinfo.parse(data, quiet=True)
        self.assertEqual(result['fanotify'], expected)


if __name__ == '__main__':
    unittest.main()
