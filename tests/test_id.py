import os
import json
import unittest
import jc.parsers.id

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/id.out'), 'r', encoding='utf-8') as f:
        centos_7_7_id = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/id.out'), 'r', encoding='utf-8') as f:
        osx_10_14_6_id = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/centos-7.7/id.json'), 'r', encoding='utf-8') as f:
        centos_7_7_id_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/osx-10.14.6/id.json'), 'r', encoding='utf-8') as f:
        osx_10_14_6_id_json = json.loads(f.read())


    def test_id_nodata(self):
        """
        Test 'id' with no data
        """
        self.assertEqual(jc.parsers.id.parse('', quiet=True), {})

    def test_id_no_name(self):
        """
        Test 'id' with no name
        """
        self.assertEqual(
            jc.parsers.id.parse('uid=1000 gid=1000 groups=1000,10', quiet=True),
            {'uid': {'id': 1000, 'name': None}, 'gid': {'id': 1000, 'name': None}, 'groups': [{'id': 1000, 'name': None}, {'id': 10, 'name': None}]}
        )

        self.assertEqual(
            jc.parsers.id.parse('uid=1000(user) gid=1000 groups=1000,10(wheel)', quiet=True),
            {'uid': {'id': 1000, 'name': 'user'}, 'gid': {'id': 1000, 'name': None}, 'groups': [{'id': 1000, 'name': None}, {'id': 10, 'name': 'wheel'}]}
        )

    def test_id_space(self):
        """
        Test 'id' with with space in name
        """
        self.assertEqual(
            jc.parsers.id.parse('uid=1000(user 1) gid=1000 groups=1000,10(wheel)', quiet=True),
            {'uid': {'id': 1000, 'name': 'user 1'}, 'gid': {'id': 1000, 'name': None}, 'groups': [{'id': 1000, 'name': None}, {'id': 10, 'name': 'wheel'}]}
        )

        self.assertEqual(
            jc.parsers.id.parse('uid=1000(user) gid=1000(group 1) groups=1000,10(wheel)', quiet=True),
            {'uid': {'id': 1000, 'name': 'user'}, 'gid': {'id': 1000, 'name': 'group 1'}, 'groups': [{'id': 1000, 'name': None}, {'id': 10, 'name': 'wheel'}]}
        )

        self.assertEqual(
            jc.parsers.id.parse('uid=1000(user) gid=1000 groups=1000,10(wheel 1)', quiet=True),
            {'uid': {'id': 1000, 'name': 'user'}, 'gid': {'id': 1000, 'name': None}, 'groups': [{'id': 1000, 'name': None}, {'id': 10, 'name': 'wheel 1'}]}
        )

        self.assertEqual(
            jc.parsers.id.parse('uid=1000(user 1) gid=1000(group 1) groups=1000,10(wheel 1)', quiet=True),
            {'uid': {'id': 1000, 'name': 'user 1'}, 'gid': {'id': 1000, 'name': 'group 1'}, 'groups': [{'id': 1000, 'name': None}, {'id': 10, 'name': 'wheel 1'}]}
        )

    def test_id_centos_7_7(self):
        """
        Test 'id' on Centos 7.7
        """
        self.assertEqual(jc.parsers.id.parse(self.centos_7_7_id, quiet=True), self.centos_7_7_id_json)

    def test_id_osx_10_14_6(self):
        """
        Test 'id' on OSX 10.14.6
        """
        self.assertEqual(jc.parsers.id.parse(self.osx_10_14_6_id, quiet=True), self.osx_10_14_6_id_json)


    def test_id_names_with_key_text(self):
        """
        Test 'id' with names that contain key, comma, and parenthesis text
        """
        self.assertEqual(
            jc.parsers.id.parse('uid=1000(ops gid=0(root)) gid=1000(ops) groups=1000(ops)', quiet=True),
            {'uid': {'id': 1000, 'name': 'ops gid=0(root)'}, 'gid': {'id': 1000, 'name': 'ops'}, 'groups': [{'id': 1000, 'name': 'ops'}]}
        )

        self.assertEqual(
            jc.parsers.id.parse('uid=1000(alice) gid=1000(alice) groups=1000(alice),2000(b,0(root)),10(wheel)', quiet=True),
            {'uid': {'id': 1000, 'name': 'alice'}, 'gid': {'id': 1000, 'name': 'alice'}, 'groups': [{'id': 1000, 'name': 'alice'}, {'id': 2000, 'name': 'b,0(root)'}, {'id': 10, 'name': 'wheel'}]}
        )

        self.assertEqual(
            jc.parsers.id.parse('uid=1000(a) gid=1000(ops gid=0(root)) groups=1000(x context=y),10(wheel) context=u:r:t:s0', quiet=True),
            {'uid': {'id': 1000, 'name': 'a'}, 'gid': {'id': 1000, 'name': 'ops gid=0(root)'}, 'groups': [{'id': 1000, 'name': 'x context=y'}, {'id': 10, 'name': 'wheel'}], 'context': {'user': 'u', 'role': 'r', 'type': 't', 'level': 's0'}}
        )

    def test_id_effective_ids(self):
        """
        Test 'id' with euid and egid fields
        """
        self.assertEqual(
            jc.parsers.id.parse('uid=0(root) gid=0(root) euid=1000(bob) egid=1000(bob) groups=0(root)', quiet=True),
            {'uid': {'id': 0, 'name': 'root'}, 'gid': {'id': 0, 'name': 'root'}, 'groups': [{'id': 0, 'name': 'root'}]}
        )


if __name__ == '__main__':
    unittest.main()
