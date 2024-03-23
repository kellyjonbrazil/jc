r"""jc - JSON Convert `update-alternatives --query` command output parser

Usage (cli):

    $ update-alternatives --query | jc --update-alt-q

or

    $ jc update-alternatives --query

Usage (module):

    import jc
    result = jc.parse('update_alt_q',
                      update_alternatives_query_command_output)

Schema:

    {
      "name":                 string,
      "link":                 string,
      "slaves": [
        {
          "name":             string,
          "path":             string
        }
      ],
      "status":               string,
      "best":                 string,
      "value":                string,   # (null if 'none')
      "alternatives": [
        {
          "alternative":      string,
          "priority":         integer,
          "slaves": [
            {
              "name":         string,
              "path":         string
            }
          ]
        }
      ]
    }

Examples:

    $ update-alternatives --query editor | jc --update-alt-q -p
    {
      "name": "editor",
      "link": "/usr/bin/editor",
      "slaves": [
        {
          "name": "editor.1.gz",
          "path": "/usr/share/man/man1/editor.1.gz"
        },
        {
          "name": "editor.da.1.gz",
          "path": "/usr/share/man/da/man1/editor.1.gz"
        }
      ],
      "status": "auto",
      "best": "/bin/nano",
      "value": "/bin/nano",
      "alternatives": [
        {
          "alternative": "/bin/ed",
          "priority": -100,
          "slaves": [
            {
              "name": "editor.1.gz",
              "path": "/usr/share/man/man1/ed.1.gz"
            }
          ]
        },
        {
          "alternative": "/bin/nano",
          "priority": 40,
          "slaves": [
            {
              "name": "editor.1.gz",
              "path": "/usr/share/man/man1/nano.1.gz"
            }
          ]
        }
      ]
    }

    $ update-alternatives --query | jc --update-alt-q -p -r
    {
      "name": "editor",
      "link": "/usr/bin/editor",
      "slaves": [
        {
          "name": "editor.1.gz",
          "path": "/usr/share/man/man1/editor.1.gz"
        },
        {
          "name": "editor.da.1.gz",
          "path": "/usr/share/man/da/man1/editor.1.gz"
        }
      ],
      "status": "auto",
      "best": "/bin/nano",
      "value": "/bin/nano",
      "alternatives": [
        {
          "alternative": "/bin/ed",
          "priority": "-100",
          "slaves": [
            {
              "name": "editor.1.gz",
              "path": "/usr/share/man/man1/ed.1.gz"
            }
          ]
        },
        {
          "alternative": "/bin/nano",
          "priority": "40",
          "slaves": [
            {
              "name": "editor.1.gz",
              "path": "/usr/share/man/man1/nano.1.gz"
            }
          ]
        }
      ]
    }
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`update-alternatives --query` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['update-alternatives --query']
    tags = ['command']


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    int_list = {'priority'}

    if 'value' in proc_data:
        if proc_data['value'] == 'none':
            proc_data['value'] = None

    if 'alternatives' in proc_data:
        for index, alt in enumerate(proc_data['alternatives']):
            for key in alt:
                if key in int_list:
                    proc_data['alternatives'][index][key] = jc.utils.convert_to_int(proc_data['alternatives'][index][key])

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> Dict:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: Dict = {}
    slaves: List = []
    alt_obj: Dict = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            line_list = line.split(maxsplit=1)

            if line.startswith('Name: '):
                raw_output['name'] = line_list[1]
                continue

            if line.startswith('Link: '):
                raw_output['link'] = line_list[1]
                continue

            if line.startswith('Slaves:'):
                continue

            if line.startswith(' '):
                s_name = line_list[0].strip()
                s_path = line_list[1]
                slaves.append(
                    {
                        "name": s_name,
                        "path": s_path
                    }
                )
                continue

            if line.startswith('Status: '):
                if slaves:
                    raw_output['slaves'] = slaves
                    slaves = []
                raw_output['status'] = line_list[1]
                continue

            if line.startswith('Best: '):
                raw_output['best'] = line_list[1]
                continue

            if line.startswith('Value: '):
                raw_output['value'] = line_list[1]
                continue

            if line.startswith('Alternative: '):
                if not 'alternatives' in raw_output:
                    raw_output['alternatives'] = []

                if alt_obj:
                    if slaves:
                        alt_obj['slaves'] = slaves
                        slaves = []

                    raw_output['alternatives'].append(alt_obj)

                alt_obj = {"alternative": line_list[1]}
                continue

            if line.startswith('Priority: '):
                alt_obj['priority'] = line_list[1]
                continue

        if alt_obj:
            if slaves:
                alt_obj['slaves'] = slaves
            raw_output['alternatives'].append(alt_obj)

    return raw_output if raw else _process(raw_output)
