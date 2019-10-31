import os
import unittest
import jc.parsers.dig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig.out'), 'r') as f:
            self.centos_7_7_dig = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig.out'), 'r') as f:
            self.ubuntu_18_4_dig = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-x.out'), 'r') as f:
            self.centos_7_7_dig_x = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-x.out'), 'r') as f:
            self.ubuntu_18_4_dig_x = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/dig-aaaa.out'), 'r') as f:
            self.centos_7_7_dig_aaaa = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/ubuntu-18.04/dig-aaaa.out'), 'r') as f:
            self.ubuntu_18_4_dig_aaaa = f.read()

    def test_dig_centos_7_7(self):
        """
        Test 'dig' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig), [{'additional_num': '1',
                                                                      'answer': [{'class': 'IN',
                                                                                  'data': 'turner-tls.map.fastly.net.',
                                                                                  'name': 'www.cnn.com.',
                                                                                  'ttl': '5',
                                                                                  'type': 'CNAME'},
                                                                                 {'class': 'IN',
                                                                                  'data': '151.101.189.67',
                                                                                  'name': 'turner-tls.map.fastly.net.',
                                                                                  'ttl': '5',
                                                                                  'type': 'A'}],
                                                                      'answer_num': '2',
                                                                      'authority_num': '0',
                                                                      'flags': 'qr rd ra',
                                                                      'id': '44295',
                                                                      'opcode': 'QUERY',
                                                                      'query_num': '1',
                                                                      'query_time': '25 msec',
                                                                      'question': {'class': 'IN', 'name': 'www.cnn.com.', 'type': 'A'},
                                                                      'rcvd': '95',
                                                                      'server': '192.168.71.2#53(192.168.71.2)',
                                                                      'status': 'NOERROR',
                                                                      'when': 'Wed Oct 30 05:13:22 PDT 2019'},
                                                                     {'additional_num': '1',
                                                                      'answer': [{'class': 'IN',
                                                                                  'data': '216.58.194.100',
                                                                                  'name': 'www.google.com.',
                                                                                  'ttl': '5',
                                                                                  'type': 'A'}],
                                                                      'answer_num': '1',
                                                                      'authority_num': '0',
                                                                      'flags': 'qr rd ra',
                                                                      'id': '34074',
                                                                      'opcode': 'QUERY',
                                                                      'query_num': '1',
                                                                      'query_time': '25 msec',
                                                                      'question': {'class': 'IN', 'name': 'www.google.com.', 'type': 'A'},
                                                                      'rcvd': '59',
                                                                      'server': '192.168.71.2#53(192.168.71.2)',
                                                                      'status': 'NOERROR',
                                                                      'when': 'Wed Oct 30 05:13:22 PDT 2019'}])

    def test_dig_ubuntu_18_4(self):
        """
        Test 'dig' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig), [{'additional_num': '1',
                                                                       'answer': [{'class': 'IN',
                                                                                   'data': 'turner-tls.map.fastly.net.',
                                                                                   'name': 'www.cnn.com.',
                                                                                   'ttl': '5',
                                                                                   'type': 'CNAME'},
                                                                                  {'class': 'IN',
                                                                                   'data': '151.101.65.67',
                                                                                   'name': 'turner-tls.map.fastly.net.',
                                                                                   'ttl': '4',
                                                                                   'type': 'A'},
                                                                                  {'class': 'IN',
                                                                                   'data': '151.101.1.67',
                                                                                   'name': 'turner-tls.map.fastly.net.',
                                                                                   'ttl': '4',
                                                                                   'type': 'A'},
                                                                                  {'class': 'IN',
                                                                                   'data': '151.101.193.67',
                                                                                   'name': 'turner-tls.map.fastly.net.',
                                                                                   'ttl': '4',
                                                                                   'type': 'A'},
                                                                                  {'class': 'IN',
                                                                                   'data': '151.101.129.67',
                                                                                   'name': 'turner-tls.map.fastly.net.',
                                                                                   'ttl': '4',
                                                                                   'type': 'A'}],
                                                                       'answer_num': '5',
                                                                       'authority_num': '0',
                                                                       'flags': 'qr rd ra',
                                                                       'id': '52284',
                                                                       'opcode': 'QUERY',
                                                                       'query_num': '1',
                                                                       'query_time': '31 msec',
                                                                       'question': {'class': 'IN', 'name': 'www.cnn.com.', 'type': 'A'},
                                                                       'rcvd': '143',
                                                                       'server': '127.0.0.53#53(127.0.0.53)',
                                                                       'status': 'NOERROR',
                                                                       'when': 'Thu Oct 31 14:21:04 UTC 2019'},
                                                                      {'additional_num': '1',
                                                                       'answer': [{'class': 'IN',
                                                                                   'data': '172.217.1.228',
                                                                                   'name': 'www.google.com.',
                                                                                   'ttl': '5',
                                                                                   'type': 'A'}],
                                                                       'answer_num': '1',
                                                                       'authority_num': '0',
                                                                       'flags': 'qr rd ra',
                                                                       'id': '47686',
                                                                       'opcode': 'QUERY',
                                                                       'query_num': '1',
                                                                       'query_time': '32 msec',
                                                                       'question': {'class': 'IN', 'name': 'www.google.com.', 'type': 'A'},
                                                                       'rcvd': '59',
                                                                       'server': '127.0.0.53#53(127.0.0.53)',
                                                                       'status': 'NOERROR',
                                                                       'when': 'Thu Oct 31 14:21:04 UTC 2019'}])

    def test_dig_x_centos_7_7(self):
        """
        Test 'dig -x' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig_x), [{'additional_num': '1',
                                                                        'answer': [{'class': 'IN',
                                                                                    'data': 'one.one.one.one.',
                                                                                    'name': '1.1.1.1.in-addr.arpa.',
                                                                                    'ttl': '5',
                                                                                    'type': 'PTR'}],
                                                                        'answer_num': '1',
                                                                        'authority_num': '0',
                                                                        'flags': 'qr rd ra',
                                                                        'id': '36298',
                                                                        'opcode': 'QUERY',
                                                                        'query_num': '1',
                                                                        'query_time': '32 msec',
                                                                        'question': {'class': 'IN', 'name': '1.1.1.1.in-addr.arpa.', 'type': 'PTR'},
                                                                        'rcvd': '78',
                                                                        'server': '192.168.71.2#53(192.168.71.2)',
                                                                        'status': 'NOERROR',
                                                                        'when': 'Wed Oct 30 05:13:36 PDT 2019'}])

    def test_dig_x_ubuntu_18_4(self):
        """
        Test 'dig -x' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig_x), [{'additional_num': '1',
                                                                         'answer': [{'class': 'IN',
                                                                                     'data': 'one.one.one.one.',
                                                                                     'name': '1.1.1.1.in-addr.arpa.',
                                                                                     'ttl': '5',
                                                                                     'type': 'PTR'}],
                                                                         'answer_num': '1',
                                                                         'authority_num': '0',
                                                                         'flags': 'qr rd ra',
                                                                         'id': '28514',
                                                                         'opcode': 'QUERY',
                                                                         'query_num': '1',
                                                                         'query_time': '37 msec',
                                                                         'question': {'class': 'IN', 'name': '1.1.1.1.in-addr.arpa.', 'type': 'PTR'},
                                                                         'rcvd': '78',
                                                                         'server': '127.0.0.53#53(127.0.0.53)',
                                                                         'status': 'NOERROR',
                                                                         'when': 'Thu Oct 31 14:21:05 UTC 2019'}])

    def test_dig_aaaa_centos_7_7(self):
        """
        Test 'dig AAAA' on Centos 7.7
        """
        self.assertEqual(jc.parsers.dig.parse(self.centos_7_7_dig_aaaa), [{'additional_num': '1',
                                                                           'answer': [{'class': 'IN',
                                                                                       'data': '2607:f8b0:4000:808::2004',
                                                                                       'name': 'www.google.com.',
                                                                                       'ttl': '5',
                                                                                       'type': 'AAAA'}],
                                                                           'answer_num': '1',
                                                                           'authority_num': '0',
                                                                           'flags': 'qr rd ra',
                                                                           'id': '25779',
                                                                           'opcode': 'QUERY',
                                                                           'query_num': '1',
                                                                           'query_time': '28 msec',
                                                                           'question': {'class': 'IN', 'name': 'www.google.com.', 'type': 'AAAA'},
                                                                           'rcvd': '71',
                                                                           'server': '192.168.71.2#53(192.168.71.2)',
                                                                           'status': 'NOERROR',
                                                                           'when': 'Wed Oct 30 05:12:53 PDT 2019'}])

    def test_dig_aaaa_ubuntu_18_4(self):
        """
        Test 'dig AAAA' on Ubuntu 18.4
        """
        self.assertEqual(jc.parsers.dig.parse(self.ubuntu_18_4_dig_aaaa), [{'additional_num': '1',
                                                                            'answer': [{'class': 'IN',
                                                                                        'data': '2607:f8b0:4000:812::2004',
                                                                                        'name': 'www.google.com.',
                                                                                        'ttl': '5',
                                                                                        'type': 'AAAA'}],
                                                                            'answer_num': '1',
                                                                            'authority_num': '0',
                                                                            'flags': 'qr rd ra',
                                                                            'id': '45806',
                                                                            'opcode': 'QUERY',
                                                                            'query_num': '1',
                                                                            'query_time': '39 msec',
                                                                            'question': {'class': 'IN', 'name': 'www.google.com.', 'type': 'AAAA'},
                                                                            'rcvd': '71',
                                                                            'server': '127.0.0.53#53(127.0.0.53)',
                                                                            'status': 'NOERROR',
                                                                            'when': 'Thu Oct 31 14:21:04 UTC 2019'}])


if __name__ == '__main__':
    unittest.main()
