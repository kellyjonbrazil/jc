import os
import unittest
import json
import jc.parsers.update_alt_q

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/update-alternatives-query.out'), 'r', encoding='utf-8') as f:
        update_alternatives_query = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/update-alternatives-query2.out'), 'r', encoding='utf-8') as f:
        update_alternatives_query2 = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/update-alternatives-query.json'), 'r', encoding='utf-8') as f:
        update_alternatives_query_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/update-alternatives-query2.json'), 'r', encoding='utf-8') as f:
        update_alternatives_query2_json = json.loads(f.read())


    def test_update_alt_q_nodata(self):
        """
        Test 'update-alternatives --query' with no data
        """
        self.assertEqual(jc.parsers.update_alt_q.parse('', quiet=True), {})

    def test_update_alt_q(self):
        """
        Test 'update-alternatives --query'
        """
        self.assertEqual(jc.parsers.update_alt_q.parse(self.update_alternatives_query, quiet=True), self.update_alternatives_query_json)

    def test_update_alt_q_no_slaves(self):
        """
        Test 'update-alternatives --query' with no slaves in output
        """
        self.assertEqual(jc.parsers.update_alt_q.parse(self.update_alternatives_query2, quiet=True), self.update_alternatives_query2_json)


if __name__ == '__main__':
    unittest.main()
