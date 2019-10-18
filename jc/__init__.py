"""JC - JSON CLI output utility

* kellyjonbrazil@gmail.com

This module serializes standard unix command line output to structured JSON
output.

Example:

$ ls -al | jc | jq .
[
    {
        "filename": ".",
        "suffix": Null,
        "bytes": 224,
        "date_updated": "Oct  1 12:09",
        "owner_user": "joeuser",
        "owner_group": "staff",
        "flags": "drwxr-xr-x+",
        "link_to": Null,
        "links": 47
    },
    {
        "filename": "..",
        "suffix": Null,
        "bytes": 224,
        "date_updated": "Oct  1 12:09",
        "owner_user": "admin",
        "owner_group": "root",
        "flags": "drwxr-xr-x",
        "link_to": Null,
        "links": 7
    },
    {
        "filename": "testfile.txt",
        "suffix": "txt",
        "bytes": 14686,
        "date_updated": "Oct  1 12:09",
        "owner_user": "joeuser",
        "owner_group": "staff",
        "flags": "-rwxr-xr-x@",
        "link_to": Null,
        "links": 1
    },
    {
        "filename": "ncat",
        "suffix": Null,
        "bytes": 14686,
        "date_updated": "Oct  1 12:09",
        "owner_user": "joeuser",
        "owner_group": "staff",
        "flags": "lrwxr-xr-x",
        "link_to": "../Cellar/nmap/7.70/bin/ncat",
        "links": 1
    }
]
"""

name = 'jc'
