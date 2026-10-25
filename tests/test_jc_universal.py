import unittest
from jc.parsers.universal import sparse_table_parse


class MyTests(unittest.TestCase):

    def test_sparse_table_parse_docstring_example(self):
        """
        Test sparse_table_parse with blank cells and spaces in cells
        """
        data = [
            'col_1        col_2     col_3     col_4         col_5',
            'apple        orange              fuzzy peach   my favorite fruits',
            'green beans            celery    spinach       my favorite veggies',
            'chicken      beef                brown eggs    my favorite proteins'
        ]
        expected = [
            {'col_1': 'apple', 'col_2': 'orange', 'col_3': None, 'col_4': 'fuzzy peach', 'col_5': 'my favorite fruits'},
            {'col_1': 'green beans', 'col_2': None, 'col_3': 'celery', 'col_4': 'spinach', 'col_5': 'my favorite veggies'},
            {'col_1': 'chicken', 'col_2': 'beef', 'col_3': None, 'col_4': 'brown eggs', 'col_5': 'my favorite proteins'}
        ]
        self.assertEqual(sparse_table_parse(data), expected)

    def test_sparse_table_parse_header_only(self):
        """
        Test sparse_table_parse with only a header row
        """
        self.assertEqual(sparse_table_parse(['a   b   c']), [])

    def test_sparse_table_parse_iterable_input(self):
        """
        Test sparse_table_parse with a generator and check that a list
        passed in is not changed
        """
        data = ['a   b', '1   2']
        self.assertEqual(sparse_table_parse(x for x in data), [{'a': '1', 'b': '2'}])
        sparse_table_parse(data)
        self.assertEqual(data, ['a   b', '1   2'])

    def test_sparse_table_parse_data_crosses_column_end(self):
        """
        Test sparse_table_parse with data that is wider than its column. When
        the search for whitespace reaches the start of the line, the first
        character is replaced by the delimiter.
        """
        data = [
            'col_1 col_2 col_3',
            'a     bbbbbbbbb c',
            'aaaaaaaaaaaaaaaaa',
            'aaaaaaaaaaa bbbbbbbbbbbb c'
        ]
        expected = [
            {'col_1': 'a', 'col_2': None, 'col_3': 'bbbbbbbbb c'},
            {'col_1': None, 'col_2': 'aaaaaaaaaaaaaaaa'},
            {'col_1': None, 'col_2': 'aaaaaaaaaa', 'col_3': 'bbbbbbbbbbbb c'}
        ]
        self.assertEqual(sparse_table_parse(data), expected)

    def test_sparse_table_parse_short_and_long_rows(self):
        """
        Test sparse_table_parse with rows shorter and longer than the header
        """
        data = [
            'name    size    note',
            'a',
            'b       12',
            '        ',
            'c       3       this note is much longer than the header row',
            'd                                                  far right'
        ]
        expected = [
            {'name': 'a', 'size': None, 'note': None},
            {'name': 'b', 'size': '12', 'note': None},
            {'name': None, 'size': None, 'note': None},
            {'name': 'c', 'size': '3', 'note': 'this note is much longer than the header row'},
            {'name': 'd', 'size': None, 'note': 'far right'}
        ]
        self.assertEqual(sparse_table_parse(data), expected)

    def test_sparse_table_parse_unicode(self):
        """
        Test sparse_table_parse with non-ASCII header names and data
        """
        data = [
            'größe   名前    note',
            '12 KB   漢字    ünïcode text',
            '        ж'
        ]
        expected = [
            {'größe': '12 KB', '名前': '漢字', 'note': 'ünïcode text'},
            {'größe': None, '名前': 'ж', 'note': None}
        ]
        self.assertEqual(sparse_table_parse(data), expected)

    def test_sparse_table_parse_delimiter_in_data(self):
        """
        Test sparse_table_parse with the delimiter character inside the data
        and with a custom delimiter
        """
        data = [
            'a      b      c      d',
            'x⁣y',
            'x      y|z'
        ]
        expected = [
            {'a': 'x', 'b': 'y', 'c': None, 'd': '⁣'},
            {'a': 'x', 'b': 'y|z', 'c': None, 'd': None}
        ]
        self.assertEqual(sparse_table_parse(data), expected)

        expected_custom = [
            {'a': 'x⁣y', 'b': None, 'c': None, 'd': None},
            {'a': 'x', 'b': 'y', 'c': 'z', 'd': '|'}
        ]
        self.assertEqual(sparse_table_parse(data, delim='|'), expected_custom)

    def test_sparse_table_parse_repeated_column_name(self):
        """
        Test sparse_table_parse finds each column at its own position in the
        header and not at the first column with the same name
        """
        data = [
            'a   b   c   b   d',
            '1   2   3   4   5'
        ]
        self.assertEqual(sparse_table_parse(data), [{'a': '1', 'b': '4', 'c': '3', 'd': '5'}])

    def test_sparse_table_parse_tab_separated_header(self):
        """
        Test sparse_table_parse with header names separated by tabs
        """
        data = [
            '\t'.join(f'col_{i:02}' for i in range(64)),
            '\t'.join(f'val_{i:02}' for i in range(64))
        ]
        expected = [{f'col_{i:02}': f'val_{i:02}' for i in range(64)}]
        self.assertEqual(sparse_table_parse(data), expected)

    def test_sparse_table_parse_many_columns(self):
        """
        Test sparse_table_parse with thousands of columns and short rows,
        rows without whitespace, and repeated column names
        """
        names = [f'c{i}' for i in range(2000)]
        expected_row = dict.fromkeys(names)
        expected_row['c0'] = 'b'
        data = [' '.join(names)] + ['b'] * 100
        self.assertEqual(sparse_table_parse(data), [expected_row] * 100)

        data = [' '.join(names)] + ['b' * 20000] * 20
        self.assertEqual(sparse_table_parse(data), [{'c0': None, 'c1': 'b' * 19999}] * 20)

        data = ['a ' * 2000] + ['b'] * 100
        self.assertEqual(sparse_table_parse(data), [{'a': None}] * 100)


if __name__ == '__main__':
    unittest.main()
