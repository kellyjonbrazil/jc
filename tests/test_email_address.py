import unittest
import json
import jc.parsers.email_address


class MyTests(unittest.TestCase):
    def test_email_address_nodata(self):
        """
        Test 'email_address' with no data
        """
        self.assertEqual(jc.parsers.email_address.parse('', quiet=True), {})


    def test_simple_email(self):
        """
        Test simple email address
        """
        data = r'fred@example.com'
        expected = json.loads(r'''{"username":"fred","domain":"example.com","local":"fred","local_plus_suffix":null}''')
        self.assertEqual(jc.parsers.email_address.parse(data, quiet=True), expected)


    def test_plus_email(self):
        """
        Test email address with plus syntax
        """
        data = r'fred+spam@example.com'
        expected = json.loads(r'''{"username":"fred","domain":"example.com","local":"fred+spam","local_plus_suffix":"spam"}''')
        self.assertEqual(jc.parsers.email_address.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
