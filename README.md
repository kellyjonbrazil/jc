# JC
JSON CLI output utility
v0.1

`jc` is used to JSONify the output of many standard linux cli tools for easier parsing in scripts. Parsers for `ls`, `ifconfig`, and `netstat` are currently included and more can be added via modules.

## Usage
`jc` accepts piped input from `STDIN` and outputs a JSON representation of the previous command to `STDOUT`. The JSON output can be compact or pretty formatted.

The first argument is required and identifies the command that is piping output to `jc` input. For example:
- `--ls` enables the `ls` parser
- `--ifconfig` enables the `ifconfig` parser
- `--netstat` enables the `netstat` parser

The second `-p` argument is optional and specifies whether to pretty format the JSON output.

## Examples
```
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
```



