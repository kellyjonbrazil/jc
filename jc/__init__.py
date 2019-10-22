"""JC - JSON CLI output utility

* kellyjonbrazil@gmail.com

This module serializes standard unix command line output to structured JSON
output.

CLI Example:

$ ls -l /bin | jc --ls -p
[
  {
    "filename": "bash",
    "flags": "-r-xr-xr-x",
    "links": 1,
    "owner": "root",
    "group": "wheel",
    "bytes": 618416,
    "date": "May 3 22:26"
  },
  {
    "filename": "cat",
    "flags": "-rwxr-xr-x",
    "links": 1,
    "owner": "root",
    "group": "wheel",
    "bytes": 23648,
    "date": "May 3 22:26"
  },
  {
    "filename": "chmod",
    "flags": "-rwxr-xr-x",
    "links": 1,
    "owner": "root",
    "group": "wheel",
    "bytes": 30016,
    "date": "May 3 22:26"
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
[{'filename': 'cat', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 
'bytes': 23648, 'date': 'May 3 22:26'}, {'filename': 'chmod', 'flags': '-rwxr-xr-x', 'links': 1, 
'owner': 'root', 'group': 'wheel', 'bytes': 30016, 'date': 'May 3 22:26'}, {'filename': 'cp', 
'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'bytes': 29024, 
'date': 'May 3 22:26'}, {'filename': 'csh', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 
'group': 'wheel', 'bytes': 375824, 'date': 'May 3 22:26'}, {'filename': 'date', 
'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 'bytes': 28608, 
'date': 'May 3 22:26'}, {'filename': 'dd', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 
'group': 'wheel', 'bytes': 32000, 'date': 'May 3 22:26'}, {'filename': 'df', 'flags': '-rwxr-xr-x', 
'links': 1, 'owner': 'root', 'group': 'wheel', 'bytes': 23392, 'date': 'May 3 22:26'}, 
{'filename': 'echo', 'flags': '-rwxr-xr-x', 'links': 1, 'owner': 'root', 'group': 'wheel', 
'bytes': 18128, 'date': 'May 3 22:26'}]
"""

name = 'jc'
