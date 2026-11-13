import os
import unittest
import json
import jc.parsers.postconf

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/postconf-M.out'), 'r', encoding='utf-8') as f:
        generic_postconf_m = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/postconf-M.json'), 'r', encoding='utf-8') as f:
        generic_postconf_m_json = json.loads(f.read())


    def test_postconf_line_separators(self):
        """
        Test 'postconf -M' with line-break characters other than LF in a command
        """
        data = 'smtp       inet  n       -       y       -       -       smtpd -o x=a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j\npickup     unix  n       -       y       60      1       pickup\n'
        result = jc.parsers.postconf.parse(data, quiet=True)
        self.assertEqual(result[0]['command'], 'smtpd -o x=a\rb\x0bc\x0cd\x1ce\x1df\x1eg\x85h\u2028i\u2029j')
        self.assertEqual(result[1]['wake_up_time'], 60)

    def test_postconf_nodata(self):
        """
        Test 'postconf' with no data
        """
        self.assertEqual(jc.parsers.postconf.parse('', quiet=True), [])

    def test_postconf(self):
        """
        Test 'postconf -M'
        """
        self.assertEqual(jc.parsers.postconf.parse(self.generic_postconf_m, quiet=True), self.generic_postconf_m_json)


if __name__ == '__main__':
    unittest.main()
