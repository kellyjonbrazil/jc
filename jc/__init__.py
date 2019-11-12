"""JC - JSON CLI output utility

* kellyjonbrazil@gmail.com

This package serializes the output of many standard unix command line tools to JSON format.

CLI Example:

    $ ls -l /usr/bin | jc --ls -p
    [
      {
        "filename": "apropos",
        "link_to": "whatis",
        "flags": "lrwxrwxrwx.",
        "links": 1,
        "owner": "root",
        "group": "root",
        "size": 6,
        "date": "Aug 15 10:53"
      },
      {
        "filename": "ar",
        "flags": "-rwxr-xr-x.",
        "links": 1,
        "owner": "root",
        "group": "root",
        "size": 62744,
        "date": "Aug 8 16:14"
      },
      {
        "filename": "arch",
        "flags": "-rwxr-xr-x.",
        "links": 1,
        "owner": "root",
        "group": "root",
        "size": 33080,
        "date": "Aug 19 23:25"
      },
      ...
    ]

Module Example:

    >>> import jc.parsers.ls
    >>> 
    >>> data='''-rwxr-xr-x  1 root  wheel    23648 May  3 22:26 cat
    ... -rwxr-xr-x  1 root  wheel    30016 May  3 22:26 chmod
    ... -rwxr-xr-x  1 root  wheel    29024 May  3 22:26 cp
    ... -rwxr-xr-x  1 root  wheel   375824 May  3 22:26 csh
    ... -rwxr-xr-x  1 root  wheel    28608 May  3 22:26 date
    ... -rwxr-xr-x  1 root  wheel    32000 May  3 22:26 dd
    ... -rwxr-xr-x  1 root  wheel    23392 May  3 22:26 df
    ... -rwxr-xr-x  1 root  wheel    18128 May  3 22:26 echo'''
    >>>
    >>> jc.parsers.ls.parse(data)
    [{'filename': 'cat', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': 23648,
    'date': 'May 3 22:26'}, {'filename': 'chmod', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root',
    'group': 'wheel', 'size': 30016, 'date': 'May 3 22:26'}, {'filename': 'cp', 'flags': '-rwxr-xr-x',
    'links': 1, 'owner': 'root', 'group': 'wheel', 'size': 29024, 'date': 'May 3 22:26'}, {'filename': 'csh',
    'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': 375824, 'date': 'May 3
    22:26'}, {'filename': 'date', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel',
    'size': 28608, 'date': 'May 3 22:26'}, {'filename': 'dd', 'flags': '-rwxr-xr-x', 'links': 1, 'owner':
    'root', 'group': 'wheel', 'size': 32000, 'date': 'May 3 22:26'}, {'filename': 'df', 'flags':
    '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': 23392, 'date': 'May 3 22:26'},
    {'filename': 'echo', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'size': 18128,
    'date': 'May 3 22:26'}]
"""

name = 'jc'
