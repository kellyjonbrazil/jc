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
        Test sparse_table_parse with data that is wider than its column.
        When the search for whitespace reaches the start of the line, the
        value moves one column to the right.
        """
        data = [
            'col_1 col_2 col_3',
            'a     bbbbbbbbb c',
            'aaaaaaaaaaaaaaaaa',
            'aaaaaaaaaaa bbbbbbbbbbbb c'
        ]
        expected = [
            {'col_1': 'a', 'col_2': None, 'col_3': 'bbbbbbbbb c'},
            {'col_1': None, 'col_2': 'aaaaaaaaaaaaaaaaa'},
            {'col_1': None, 'col_2': 'aaaaaaaaaaa', 'col_3': 'bbbbbbbbbbbb c'}
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
        Test sparse_table_parse with delimiter characters inside the data
        """
        data = [
            'a      b      c      d',
            'x\u2063y',
            'x      y|z',
            'x\u20631\u20632    v      w\u2063\x00      z',
            '\x00\u2063'
        ]
        expected = [
            {'a': 'x\u2063y', 'b': None, 'c': None, 'd': None},
            {'a': 'x', 'b': 'y|z', 'c': None, 'd': None},
            {'a': 'x\u20631\u20632', 'b': 'v', 'c': 'w\u2063\x00', 'd': 'z'},
            {'a': '\x00\u2063', 'b': None, 'c': None, 'd': None}
        ]
        self.assertEqual(sparse_table_parse(data), expected)
        self.assertEqual(sparse_table_parse(data, delim='|'), expected)
        self.assertEqual(sparse_table_parse(data, delim='\x00'), expected)

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
        self.assertEqual(sparse_table_parse(data), [{'c0': None, 'c1': 'b' * 20000}] * 20)

        data = ['a ' * 2000] + ['b'] * 100
        self.assertEqual(sparse_table_parse(data), [{'a': None}] * 100)


    def test_sparse_table_parse_display_width(self):
        """
        Test sparse_table_parse measures column positions in display cells
        """
        data = [
            'name      label     size',
            '\u5171\u6709\u30e1\u30e2  x         10',
            'a\u200bb       cafe\u0301      20',
            'c\ufeff         \u65e5\u672c\u8a9e\u30e9  30',
            'd         e\u0301\u0302\u2063f        40'
        ]
        expected = [
            {'name': '\u5171\u6709\u30e1\u30e2', 'label': 'x', 'size': '10'},
            {'name': 'a\u200bb', 'label': 'cafe\u0301', 'size': '20'},
            {'name': 'c\ufeff', 'label': '\u65e5\u672c\u8a9e\u30e9', 'size': '30'},
            {'name': 'd', 'label': 'e\u0301\u0302\u2063f', 'size': '40'}
        ]
        self.assertEqual(sparse_table_parse(data), expected)

    def test_sparse_table_parse_wide_header(self):
        """
        Test sparse_table_parse with wide characters in the header row
        """
        data = [
            '\u540d\u524d  \u30b5\u30a4\u30ba  note',
            'ab    12        x y',
            '\u5171\u6709  3\u0301        \u65e5'
        ]
        expected = [
            {'\u540d\u524d': 'ab', '\u30b5\u30a4\u30ba': '12', 'note': 'x y'},
            {'\u540d\u524d': '\u5171\u6709', '\u30b5\u30a4\u30ba': '3\u0301', 'note': '\u65e5'}
        ]
        self.assertEqual(sparse_table_parse(data), expected)

    def test_sparse_table_parse_value_from_line_start(self):
        """
        Test 'sparse_table_parse' with a value that starts the line and runs past its column
        """
        data = ['a    b    c', 'longvalue x', ' ongvalue x', 'q    r    t']
        expected = [
            {'a': None, 'b': 'longvalue', 'c': 'x'},
            {'a': None, 'b': 'ongvalue', 'c': 'x'},
            {'a': 'q', 'b': 'r', 'c': 't'}
        ]
        self.assertEqual(sparse_table_parse(data), expected)


if __name__ == '__main__':
    unittest.main()
