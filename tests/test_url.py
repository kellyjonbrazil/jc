import unittest
import json
import jc.parsers.url


class MyTests(unittest.TestCase):
    def test_url_nodata(self):
        """
        Test 'url' with no data
        """
        self.assertEqual(jc.parsers.url.parse('', quiet=True), {})


    def test_url_mailto(self):
        """
        Test mailto URL
        """
        data = r'<mailto:fred@example.com>'
        expected = json.loads(r'''{"url":"mailto:fred@example.com","scheme":"mailto","netloc":null,"path":"fred@example.com","parent":".","filename":"fred@example.com","stem":"fred@example","extension":"com","path_list":["fred@example.com"],"query":null,"query_obj":null,"fragment":null,"username":null,"password":null,"hostname":null,"port":null,"encoded":{"url":"mailto:fred@example.com","scheme":"mailto","netloc":null,"path":"fred@example.com","parent":".","filename":"fred@example.com","stem":"fred@example","extension":"com","path_list":["fred@example.com"],"query":null,"fragment":null,"username":null,"password":null,"hostname":null,"port":null},"decoded":{"url":"mailto:fred@example.com","scheme":"mailto","netloc":null,"path":"fred@example.com","parent":".","filename":"fred@example.com","stem":"fred@example","extension":"com","path_list":["fred@example.com"],"query":null,"fragment":null,"username":null,"password":null,"hostname":null,"port":null}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_ftp(self):
        """
        Test ftp URL
        """
        data = r'ftp://localhost/filepath/filename.txt'
        expected = json.loads(r'''{"url":"ftp://localhost/filepath/filename.txt","scheme":"ftp","netloc":"localhost","path":"/filepath/filename.txt","parent":"/filepath","filename":"filename.txt","stem":"filename","extension":"txt","path_list":["filepath","filename.txt"],"query":null,"query_obj":null,"fragment":null,"username":null,"password":null,"hostname":"localhost","port":null,"encoded":{"url":"ftp://localhost/filepath/filename.txt","scheme":"ftp","netloc":"localhost","path":"/filepath/filename.txt","parent":"/filepath","filename":"filename.txt","stem":"filename","extension":"txt","path_list":["filepath","filename.txt"],"query":null,"fragment":null,"username":null,"password":null,"hostname":"localhost","port":null},"decoded":{"url":"ftp://localhost/filepath/filename.txt","scheme":"ftp","netloc":"localhost","path":"/filepath/filename.txt","parent":"/filepath","filename":"filename.txt","stem":"filename","extension":"txt","path_list":["filepath","filename.txt"],"query":null,"fragment":null,"username":null,"password":null,"hostname":"localhost","port":null}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_http_ipv4(self):
        """
        Test HTTP URL with encodable characters (ipv4 host)
        """
        data = r'<URL:http://user{one:pass{two@127.0.0.1:8000/a space/b/c/d?q1=foo with {space}&q2=bar&q2=baz#frag{frag>'
        expected = json.loads(r'''{"url":"http://user{one:pass{two@127.0.0.1:8000/a space/b/c/d?q1=foo with {space}&q2=bar&q2=baz#frag{frag","scheme":"http","netloc":"user{one:pass{two@127.0.0.1:8000","path":"/a space/b/c/d","parent":"/a space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a space","b","c","d"],"query":"q1=foo with {space}&q2=bar&q2=baz","query_obj":{"q1":["foo with {space}"],"q2":["bar","baz"]},"fragment":"frag{frag","username":"user{one","password":"pass{two","hostname":"127.0.0.1","port":8000,"encoded":{"url":"http://user%7Bone:pass%7Btwo@127.0.0.1:8000/a%20space/b/c/d?q1=foo+with+%7Bspace%7D&q2=bar&q2=baz#frag%7Bfrag","scheme":"http","netloc":"user%7Bone:pass%7Btwo@127.0.0.1:8000","path":"/a%20space/b/c/d","parent":"/a%20space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a%20space","b","c","d"],"query":"q1=foo+with+%7Bspace%7D&q2=bar&q2=baz","fragment":"frag%7Bfrag","username":"user%7Bone","password":"pass%7Btwo","hostname":"127.0.0.1","port":8000},"decoded":{"url":"http://user{one:pass{two@127.0.0.1:8000/a space/b/c/d?q1=foo with {space}&q2=bar&q2=baz#frag{frag","scheme":"http","netloc":"user{one:pass{two@127.0.0.1:8000","path":"/a space/b/c/d","parent":"/a space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a space","b","c","d"],"query":"q1=foo with {space}&q2=bar&q2=baz","fragment":"frag{frag","username":"user{one","password":"pass{two","hostname":"127.0.0.1","port":8000}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_http_ipv6(self):
        """
        Test HTTP URL with encodable characters (ipv6 host)
        """
        data = r'<URL:http://user{one:pass{two@[1:2::127]:8000/a space/b/c/d?q1=foo with {space}&q2=bar&q2=baz#frag{frag>'
        expected = json.loads(r'''{"url":"http://user{one:pass{two@[1:2::127]:8000/a space/b/c/d?q1=foo with {space}&q2=bar&q2=baz#frag{frag","scheme":"http","netloc":"user{one:pass{two@[1:2::127]:8000","path":"/a space/b/c/d","parent":"/a space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a space","b","c","d"],"query":"q1=foo with {space}&q2=bar&q2=baz","query_obj":{"q1":["foo with {space}"],"q2":["bar","baz"]},"fragment":"frag{frag","username":"user{one","password":"pass{two","hostname":"1:2::127","port":8000,"encoded":{"url":"http://user%7Bone:pass%7Btwo@[1:2::127]:8000/a%20space/b/c/d?q1=foo+with+%7Bspace%7D&q2=bar&q2=baz#frag%7Bfrag","scheme":"http","netloc":"user%7Bone:pass%7Btwo@[1:2::127]:8000","path":"/a%20space/b/c/d","parent":"/a%20space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a%20space","b","c","d"],"query":"q1=foo+with+%7Bspace%7D&q2=bar&q2=baz","fragment":"frag%7Bfrag","username":"user%7Bone","password":"pass%7Btwo","hostname":"1:2::127","port":8000},"decoded":{"url":"http://user{one:pass{two@[1:2::127]:8000/a space/b/c/d?q1=foo with {space}&q2=bar&q2=baz#frag{frag","scheme":"http","netloc":"user{one:pass{two@[1:2::127]:8000","path":"/a space/b/c/d","parent":"/a space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a space","b","c","d"],"query":"q1=foo with {space}&q2=bar&q2=baz","fragment":"frag{frag","username":"user{one","password":"pass{two","hostname":"1:2::127","port":8000}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_http_domain(self):
        """
        Test HTTP URL with encodable characters (domain name host)
        """
        data = r'<URL:http://user{one:pass{two@www.example.com:8000/a space/b/c/d?q1=foo with {space}&q2=bar&q2=baz#frag{frag>'
        expected = json.loads(r'''{"url":"http://user{one:pass{two@www.example.com:8000/a space/b/c/d?q1=foo with {space}&q2=bar&q2=baz#frag{frag","scheme":"http","netloc":"user{one:pass{two@www.example.com:8000","path":"/a space/b/c/d","parent":"/a space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a space","b","c","d"],"query":"q1=foo with {space}&q2=bar&q2=baz","query_obj":{"q1":["foo with {space}"],"q2":["bar","baz"]},"fragment":"frag{frag","username":"user{one","password":"pass{two","hostname":"www.example.com","port":8000,"encoded":{"url":"http://user%7Bone:pass%7Btwo@www.example.com:8000/a%20space/b/c/d?q1=foo+with+%7Bspace%7D&q2=bar&q2=baz#frag%7Bfrag","scheme":"http","netloc":"user%7Bone:pass%7Btwo@www.example.com:8000","path":"/a%20space/b/c/d","parent":"/a%20space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a%20space","b","c","d"],"query":"q1=foo+with+%7Bspace%7D&q2=bar&q2=baz","fragment":"frag%7Bfrag","username":"user%7Bone","password":"pass%7Btwo","hostname":"www.example.com","port":8000},"decoded":{"url":"http://user{one:pass{two@www.example.com:8000/a space/b/c/d?q1=foo with {space}&q2=bar&q2=baz#frag{frag","scheme":"http","netloc":"user{one:pass{two@www.example.com:8000","path":"/a space/b/c/d","parent":"/a space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a space","b","c","d"],"query":"q1=foo with {space}&q2=bar&q2=baz","fragment":"frag{frag","username":"user{one","password":"pass{two","hostname":"www.example.com","port":8000}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_http_encoded(self):
        """
        Test HTTP URL with encoded characters
        """
        data = r'http://user%7Bone:pass%7Btwo@www.example.com:8000/a%20space/b/c/d?q1=foo+with+%7Bspace%7D&q2=bar&q2=baz#frag%7Bfrag'
        expected = json.loads(r'''{"url":"http://user%7Bone:pass%7Btwo@www.example.com:8000/a%20space/b/c/d?q1=foo+with+%7Bspace%7D&q2=bar&q2=baz#frag%7Bfrag","scheme":"http","netloc":"user%7Bone:pass%7Btwo@www.example.com:8000","path":"/a%20space/b/c/d","parent":"/a%20space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a%20space","b","c","d"],"query":"q1=foo+with+%7Bspace%7D&q2=bar&q2=baz","query_obj":{"q1":["foo with {space}"],"q2":["bar","baz"]},"fragment":"frag%7Bfrag","username":"user%7Bone","password":"pass%7Btwo","hostname":"www.example.com","port":8000,"encoded":{"url":"http://user%257Bone:pass%257Btwo@www.example.com:8000/a%2520space/b/c/d?q1=foo+with+%257Bspace%257D&q2=bar&q2=baz#frag%257Bfrag","scheme":"http","netloc":"user%257Bone:pass%257Btwo@www.example.com:8000","path":"/a%2520space/b/c/d","parent":"/a%2520space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a%2520space","b","c","d"],"query":"q1=foo+with+%257Bspace%257D&q2=bar&q2=baz","fragment":"frag%257Bfrag","username":"user%257Bone","password":"pass%257Btwo","hostname":"www.example.com","port":8000},"decoded":{"url":"http://user{one:pass{two@www.example.com:8000/a space/b/c/d?q1=foo with {space}&q2=bar&q2=baz#frag{frag","scheme":"http","netloc":"user{one:pass{two@www.example.com:8000","path":"/a space/b/c/d","parent":"/a space/b/c","filename":"d","stem":"d","extension":null,"path_list":["a space","b","c","d"],"query":"q1=foo with {space}&q2=bar&q2=baz","fragment":"frag{frag","username":"user{one","password":"pass{two","hostname":"www.example.com","port":8000}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_http_encodable_host_and_port(self):
        """
        Test HTTP URL with encodable characters in the hostname and port
        """
        data = r'http://хост.домен:8080'
        expected = json.loads(r'''{"url":"http://хост.домен:8080","scheme":"http","netloc":"хост.домен:8080","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"query_obj":null,"fragment":null,"username":null,"password":null,"hostname":"хост.домен","port":8080,"encoded":{"url":"http://%D1%85%D0%BE%D1%81%D1%82.%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD:8080","scheme":"http","netloc":"%D1%85%D0%BE%D1%81%D1%82.%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD:8080","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"fragment":null,"username":null,"password":null,"hostname":"%D1%85%D0%BE%D1%81%D1%82.%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD","port":8080},"decoded":{"url":"http://хост.домен:8080","scheme":"http","netloc":"хост.домен:8080","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"fragment":null,"username":null,"password":null,"hostname":"хост.домен","port":8080}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_http_encoded_host_and_port(self):
        """
        Test HTTP URL with encoded characters in the hostname and port
        """
        data = r'http://%D1%85%D0%BE%D1%81%D1%82.%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD:%38%38'
        expected = json.loads(r'''{"url":"http://%D1%85%D0%BE%D1%81%D1%82.%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD:%38%38","scheme":"http","netloc":"%D1%85%D0%BE%D1%81%D1%82.%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD:%38%38","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"query_obj":null,"fragment":null,"username":null,"password":null,"hostname":"%D1%85%D0%BE%D1%81%D1%82.%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD","port":88,"encoded":{"url":"http://%25D1%2585%25D0%25BE%25D1%2581%25D1%2582.%25D0%25B4%25D0%25BE%25D0%25BC%25D0%25B5%25D0%25BD:%2538%2538","scheme":"http","netloc":"%25D1%2585%25D0%25BE%25D1%2581%25D1%2582.%25D0%25B4%25D0%25BE%25D0%25BC%25D0%25B5%25D0%25BD:%2538%2538","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"fragment":null,"username":null,"password":null,"hostname":"%25D1%2585%25D0%25BE%25D1%2581%25D1%2582.%25D0%25B4%25D0%25BE%25D0%25BC%25D0%25B5%25D0%25BD","port":88},"decoded":{"url":"http://хост.домен:88","scheme":"http","netloc":"хост.домен:88","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"fragment":null,"username":null,"password":null,"hostname":"хост.домен","port":88}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_http_encoded_host_and_invalid_port(self):
        """
        Test HTTP URL with encoded characters in the hostname and an invalid encoded port
        """
        data = r'http://хост.домен:%38{%38#frag'
        expected = json.loads(r'''{"url":"http://хост.домен:%38{%38#frag","scheme":"http","netloc":"хост.домен:%38{%38","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"query_obj":null,"fragment":"frag","username":null,"password":null,"hostname":"хост.домен","port":null,"encoded":{"url":"http://%D1%85%D0%BE%D1%81%D1%82.%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD:%2538%7B%2538#frag","scheme":"http","netloc":"%D1%85%D0%BE%D1%81%D1%82.%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD:%2538%7B%2538","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"fragment":"frag","username":null,"password":null,"hostname":"%D1%85%D0%BE%D1%81%D1%82.%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD","port":null},"decoded":{"url":"http://хост.домен:8{8#frag","scheme":"http","netloc":"хост.домен:8{8","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"fragment":"frag","username":null,"password":null,"hostname":"хост.домен","port":null}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_http_path_ends_in_slash(self):
        """
        Test HTTP URL with a forward slash as the last part of the path
        """
        data = r'https://pypi.org/project/jc/1.20.3/'
        expected = json.loads(r'''{"url":"https://pypi.org/project/jc/1.20.3/","scheme":"https","netloc":"pypi.org","path":"/project/jc/1.20.3/","parent":"/project/jc","filename":"1.20.3","stem":"1.20","extension":"3","path_list":["project","jc","1.20.3"],"query":null,"query_obj":null,"fragment":null,"username":null,"password":null,"hostname":"pypi.org","port":null,"encoded":{"url":"https://pypi.org/project/jc/1.20.3/","scheme":"https","netloc":"pypi.org","path":"/project/jc/1.20.3/","parent":"/project/jc","filename":"1.20.3","stem":"1.20","extension":"3","path_list":["project","jc","1.20.3"],"query":null,"fragment":null,"username":null,"password":null,"hostname":"pypi.org","port":null},"decoded":{"url":"https://pypi.org/project/jc/1.20.3/","scheme":"https","netloc":"pypi.org","path":"/project/jc/1.20.3/","parent":"/project/jc","filename":"1.20.3","stem":"1.20","extension":"3","path_list":["project","jc","1.20.3"],"query":null,"fragment":null,"username":null,"password":null,"hostname":"pypi.org","port":null}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_http_path_only_slash(self):
        """
        Test HTTP URL with a forward slash as the last only part of the path
        """
        data = r'https://pypi.org/'
        expected = json.loads(r'''{"url":"https://pypi.org/","scheme":"https","netloc":"pypi.org","path":"/","parent":"/","filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"query_obj":null,"fragment":null,"username":null,"password":null,"hostname":"pypi.org","port":null,"encoded":{"url":"https://pypi.org/","scheme":"https","netloc":"pypi.org","path":"/","parent":"/","filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"fragment":null,"username":null,"password":null,"hostname":"pypi.org","port":null},"decoded":{"url":"https://pypi.org/","scheme":"https","netloc":"pypi.org","path":"/","parent":"/","filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"fragment":null,"username":null,"password":null,"hostname":"pypi.org","port":null}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_http_path_no_end_slash(self):
        """
        Test HTTP URL with no forward slash at the end
        """
        data = r'https://pypi.org'
        expected = json.loads(r'''{"url":"https://pypi.org","scheme":"https","netloc":"pypi.org","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"query_obj":null,"fragment":null,"username":null,"password":null,"hostname":"pypi.org","port":null,"encoded":{"url":"https://pypi.org","scheme":"https","netloc":"pypi.org","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"fragment":null,"username":null,"password":null,"hostname":"pypi.org","port":null},"decoded":{"url":"https://pypi.org","scheme":"https","netloc":"pypi.org","path":null,"parent":null,"filename":null,"stem":null,"extension":null,"path_list":null,"query":null,"fragment":null,"username":null,"password":null,"hostname":"pypi.org","port":null}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


    def test_url_file_path(self):
        """
        Test a normal file path URL
        """
        data = r'/this/is my/path/to the file/myfile.tar.gz'
        expected = json.loads(r'''{"url":"/this/is my/path/to the file/myfile.tar.gz","scheme":null,"netloc":null,"path":"/this/is my/path/to the file/myfile.tar.gz","parent":"/this/is my/path/to the file","filename":"myfile.tar.gz","stem":"myfile.tar","extension":"gz","path_list":["this","is my","path","to the file","myfile.tar.gz"],"query":null,"query_obj":null,"fragment":null,"username":null,"password":null,"hostname":null,"port":null,"encoded":{"url":"/this/is%20my/path/to%20the%20file/myfile.tar.gz","scheme":null,"netloc":null,"path":"/this/is%20my/path/to%20the%20file/myfile.tar.gz","parent":"/this/is%20my/path/to%20the%20file","filename":"myfile.tar.gz","stem":"myfile.tar","extension":"gz","path_list":["this","is%20my","path","to%20the%20file","myfile.tar.gz"],"query":null,"fragment":null,"username":null,"password":null,"hostname":null,"port":null},"decoded":{"url":"/this/is my/path/to the file/myfile.tar.gz","scheme":null,"netloc":null,"path":"/this/is my/path/to the file/myfile.tar.gz","parent":"/this/is my/path/to the file","filename":"myfile.tar.gz","stem":"myfile.tar","extension":"gz","path_list":["this","is my","path","to the file","myfile.tar.gz"],"query":null,"fragment":null,"username":null,"password":null,"hostname":null,"port":null}}''')
        self.assertEqual(jc.parsers.url.parse(data, quiet=True), expected)


if __name__ == '__main__':
    unittest.main()
