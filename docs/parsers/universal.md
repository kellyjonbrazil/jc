
# jc.parsers.universal
jc - JSON CLI output utility universal Parsers

## simple_table_parse
```python
simple_table_parse(data)
```

Parse simple tables. The last column may contain data with spaces.

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


## sparse_table_parse
```python
sparse_table_parse(data, delim='\u2063')
```

Parse tables with missing column data or with spaces in column data.

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

    delim:  (string) Delimiter to use. By default `u\2063`
                     (invisible separator) is used since it is unlikely
                     to ever be seen in terminal output. You can change
                     this for troubleshooting purposes or if there is a
                     delimiter conflict with your data.

Returns:

    List of Dictionaries

