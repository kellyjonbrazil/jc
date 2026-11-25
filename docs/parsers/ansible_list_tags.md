[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ansible_list_tags"></a>

# jc.parsers.ansible_list_tags

jc - JSON Convert `ansible-playbook --list-tags` command output parser

Usage (cli):

    $ ansible-playbook --list-tags playbook.yaml | jc --ansible-list-tags

or

    $ jc ansible-playbook --list-tags playbook.yaml

Usage (module):

    import jc
    result = jc.parse('ansible_list_tags', ansible_playbook_command_output)

Schema:

    [
      {
        "playbook":     string,
        "plays": [
          {
            "number":     integer,
            "hosts": [
                                     string
            ],
            "name":       string,
            "tags": [
                                     string
            ],
            "task_tags": [
                                     string
            ]
          }
        ]
      }
    ]

Examples:

    $ ansible-playbook --list-tags playbook.yaml | jc --ansible-list-tags -p
    [
      {
        "playbook": "playbook.yaml",
        "plays": [
          {
            "number": 1,
            "hosts": [
              "all"
            ],
            "name": "all",
            "tags": [],
            "task_tags": []
          }
        ]
      }
    ]

<a id="jc.parsers.ansible_list_tags.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[Dict[str, Any]]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/ansible_list_tags.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/ansible_list_tags.py)

Version 1.0 by Rahul Ranjan (11793455+rahul05ranjan@users.noreply.github.com)
