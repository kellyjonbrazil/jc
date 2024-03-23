[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.universal"></a>

# jc.parsers.universal

## Table of Contents

* [jc.parsers.universal](#jc.parsers.universal)
  * [simple_table_parse](#jc.parsers.universal.simple_table_parse)
  * [sparse_table_parse](#jc.parsers.universal.sparse_table_parse)

jc - JSON Convert universal parsers

<a id="jc.parsers.universal.simple_table_parse"></a>

### simple_table_parse

```python
def simple_table_parse(data: Iterable[str]) -> List[Dict]
```

Parse simple tables. There should be no blank cells. The last column
may contain data with spaces.

Example Table:

    col_1     col_2     col_3     col_4     col_5
    apple     orange    pear      banana    my favorite fruits
    carrot    squash    celery    spinach   my favorite veggies
    chicken   beef      pork      eggs      my favorite proteins

    [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
    'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
    'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
    'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
    'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

Parameters:

    data:   (iter)   Text data to parse that has been split into lines
                     via .splitlines(). Item 0 must be the header row.
                     Any spaces in header names should be changed to
                     underscore '_'. You should also ensure headers are
                     lowercase by using .lower().

                     Also, ensure there are no blank rows in the data.

Returns:

    List of Dictionaries

<a id="jc.parsers.universal.sparse_table_parse"></a>

### sparse_table_parse

```python
def sparse_table_parse(data: Iterable[str],
                       delim: str = '\u2063') -> List[Dict]
```

Parse tables with missing column data or with spaces in column data.
Blank cells are converted to None in the resulting dictionary. Data
elements must line up within column boundaries.

Example Table:

    col_1        col_2     col_3     col_4         col_5
    apple        orange              fuzzy peach   my favorite fruits
    green beans            celery    spinach       my favorite veggies
    chicken      beef                brown eggs    my favorite proteins

    [{'col_1': 'apple', 'col_2': 'orange', 'col_3': None, 'col_4':
    'fuzzy peach', 'col_5': 'my favorite fruits'}, {'col_1':
    'green beans', 'col_2': None, 'col_3': 'celery', 'col_4': 'spinach',
    'col_5': 'my favorite veggies'}, {'col_1': 'chicken', 'col_2':
    'beef', 'col_3': None, 'col_4': 'brown eggs', 'col_5':
    'my favorite proteins'}]

Parameters:

    data:   (iter)   An iterable of string lines (e.g. str.splitlines())
                     Item 0 must be the header row. Any spaces in header
                     names should be changed to underscore '_'. You
                     should also ensure headers are lowercase by using
                     .lower(). Do not change the position of header
                     names as the positions are used to find the data.

                     Also, ensure there are no blank line items.

    delim:  (string) Delimiter to use. By default `u\2063`
                     (invisible separator) is used since it is unlikely
                     to ever be seen in terminal output. You can change
                     this for troubleshooting purposes or if there is a
                     delimiter conflict with your data.

Returns:

    List of Dictionaries


