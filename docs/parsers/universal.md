# Table of Contents

* [jc.parsers.universal](#jc.parsers.universal)
  * [simple\_table\_parse](#jc.parsers.universal.simple_table_parse)
  * [sparse\_table\_parse](#jc.parsers.universal.sparse_table_parse)

<a id="jc.parsers.universal"></a>

# jc.parsers.universal

jc - JSON Convert universal parsers

<a id="jc.parsers.universal.simple_table_parse"></a>

### simple\_table\_parse

```python
def simple_table_parse(data: List[str]) -> List[Dict]
```

Parse simple tables. There should be no blank cells. The last column
may contain data with spaces.

Example Table:

    col1      col2      col3      col4      col5
    apple     orange    pear      banana    my favorite fruits
    carrot    squash    celery    spinach   my favorite veggies
    chicken   beef      pork      eggs      my favorite proteins

Parameters:

    data:   (list)   Text data to parse that has been split into lines
                     via .splitlines(). Item 0 must be the header row.
                     Any spaces in header names should be changed to
                     underscore '_'. You should also ensure headers are
                     lowercase by using .lower().

                     Also, ensure there are no blank lines (list items)
                     in the data.

Returns:

    List of Dictionaries

<a id="jc.parsers.universal.sparse_table_parse"></a>

### sparse\_table\_parse

```python
def sparse_table_parse(data: List[str], delim: str = '\u2063') -> List[Dict]
```

Parse tables with missing column data or with spaces in column data.
Data elements must line up within column boundaries.

Example Table:

    col1         col2      col3      col4          col5
    apple        orange              fuzzy peach   my favorite fruits
    green beans            celery    spinach       my favorite veggies
    chicken      beef                brown eggs    my favorite proteins

Parameters:

    data:   (list)   Text data to parse that has been split into lines
                     via .splitlines(). Item 0 must be the header row.
                     Any spaces in header names should be changed to
                     underscore '_'. You should also ensure headers are
                     lowercase by using .lower(). Do not change the
                     position of header names as the positions are used
                     to find the data.

                     Also, ensure there are no blank lines (list items)
                     in the data.

    delim:  (string) Delimiter to use. By default `u\\2063`
                     (invisible separator) is used since it is unlikely
                     to ever be seen in terminal output. You can change
                     this for troubleshooting purposes or if there is a
                     delimiter conflict with your data.

Returns:

    List of Dictionaries

