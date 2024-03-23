[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.git_ls_remote"></a>

# jc.parsers.git_ls_remote

jc - JSON Convert `git ls-remote` command output parser

This parser outputs two schemas:

- Default: A single object with key/value pairs
- Raw: An array of objects (`--raw` (cli) or `raw=True (module))

See the Schema section for more details

Usage (cli):

    $ git ls-remote | jc --git-ls-remote

or

    $ jc git ls-remote

Usage (module):

    import jc
    result = jc.parse('git_ls_remote', git_ls_remote_command_output)

Schema:

    Default:
    {
      <reference>:            string
    }

    Raw:
    [
      {
        "reference":          string,
        "commit":             string
      }
    ]

Examples:

    $ git ls-remote | jc --git-ls-remote -p
    {
      "HEAD": "214cd6b9e09603b3c4fa02203b24fb2bc3d4e338",
      "refs/heads/dev": "b884f6aacca39e05994596d8fdfa7e7c4f1e0389",
      "refs/heads/master": "214cd6b9e09603b3c4fa02203b24fb2bc3d4e338",
      "refs/pull/1/head": "e416c77bed1267254da972b0f95b7ff1d43fccef",
      ...
    }

    $ git ls-remote | jc --git-ls-remote -p -r
    [
      {
        "reference": "HEAD",
        "commit": "214cd6b9e09603b3c4fa02203b24fb2bc3d4e338"
      },
      {
        "reference": "refs/heads/dev",
        "commit": "b884f6aacca39e05994596d8fdfa7e7c4f1e0389"
      },
      ...
    ]

<a id="jc.parsers.git_ls_remote.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> Union[Dict[str, Any], List[Dict[str, Any]]]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary (default) or List of Dictionaries (raw)

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/git_ls_remote.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/git_ls_remote.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
