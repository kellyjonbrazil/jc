import unittest
import json
import jc.parsers.jwt


class MyTests(unittest.TestCase):
    def test_jwt_nodata(self):
        """
        Test 'jwt' with no data
        """
        self.assertEqual(jc.parsers.jwt.parse('', quiet=True), {})


    def test_jwt_example(self):
        """
        Test simple jwt example
        """
        data = r'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        expected = json.loads(r'''{"header":{"alg":"HS256","typ":"JWT"},"payload":{"sub":"1234567890","name":"John Doe","iat":1516239022},"signature":"49:f9:4a:c7:04:49:48:c7:8a:28:5d:90:4f:87:f0:a4:c7:89:7f:7e:8f:3a:4e:b2:25:5f:da:75:0b:2c:c3:97"}''')
        self.assertEqual(jc.parsers.jwt.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
