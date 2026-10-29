import os
import unittest
import json
from typing import Dict
import jc.parsers.proc_version

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):
    f_in: Dict = {}
    f_json: Dict = {}

    @classmethod
    def setUpClass(cls):
        fixtures = {
            'proc_version': (
                'fixtures/linux-proc/version',
                'fixtures/linux-proc/version.json'),
            'proc_version2': (
                'fixtures/linux-proc/version2',
                'fixtures/linux-proc/version2.json'),
            'proc_version3': (
                'fixtures/linux-proc/version3',
                'fixtures/linux-proc/version3.json'),
            'proc_version_long': (
                'fixtures/generic/proc-version-long.out',
                'fixtures/generic/proc-version-long.json')
        }

        for file, filepaths in fixtures.items():
            with open(os.path.join(THIS_DIR, filepaths[0]), 'r', encoding='utf-8') as a, \
                 open(os.path.join(THIS_DIR, filepaths[1]), 'r', encoding='utf-8') as b:
                cls.f_in[file] = a.read()
                cls.f_json[file] = json.loads(b.read())


    def test_proc_version_nodata(self):
        """
        Test 'proc_version' with no data
        """
        self.assertEqual(jc.parsers.proc_version.parse('', quiet=True), {})

    def test_proc_version(self):
        """
        Test '/proc/version'
        """
        self.assertEqual(jc.parsers.proc_version.parse(self.f_in['proc_version'], quiet=True),
                                                       self.f_json['proc_version'])

    def test_proc_version2(self):
        """
        Test '/proc/version' #2
        """
        self.assertEqual(jc.parsers.proc_version.parse(self.f_in['proc_version2'], quiet=True),
                                                       self.f_json['proc_version2'])

    def test_proc_version3(self):
        """
        Test '/proc/version' #3
        """
        self.assertEqual(jc.parsers.proc_version.parse(self.f_in['proc_version3'], quiet=True),
                                                       self.f_json['proc_version3'])

    def test_proc_version_long(self):
        """
        Test '/proc/version' with a long build number and flags
        """
        self.assertEqual(jc.parsers.proc_version.parse(self.f_in['proc_version_long'], quiet=True),
                                                       self.f_json['proc_version_long'])

    def test_proc_version_debian_date(self):
        """
        Test '/proc/version' with the date format Debian uses
        """
        data = 'Linux version 6.1.0-18-amd64 (debian-kernel@lists.debian.org) (gcc-12 (Debian 12.2.0-14) 12.2.0, GNU ld (GNU Binutils for Debian) 2.40) #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01)\n'
        self.assertEqual(jc.parsers.proc_version.parse(data, quiet=True), {
            'version': '6.1.0-18-amd64',
            'email': 'debian-kernel@lists.debian.org',
            'gcc': 'gcc-12 (Debian 12.2.0-14) 12.2.0, GNU ld (GNU Binutils for Debian) 2.40',
            'build': '#1',
            'flags': 'SMP PREEMPT_DYNAMIC Debian 6.1.76-1',
            'date': '2024-02-01'
        })


if __name__ == '__main__':
    unittest.main()
