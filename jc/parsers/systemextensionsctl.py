"""jc - JSON Convert `systemextensionsctl list` command output parser

Usage:

    $ systemextensionsctl list | jc --systemextensionsctl

Compatibility:

    macOS

Example:

    $ systemextensionsctl list | jc --systemextensionsctl -p
    {
      "total_extensions": 1,
      "sections": [
        {
          "category": "com.apple.system_extension.network_extension",
          "description": "Go to 'System Settings > General > Login Items & Extensions > Network Extensions' to modify these system extension(s)",
          "entries": [
            {
              "enabled": "*",
              "active": "*",
              "teamID": "XXX",
              "bundleID": "YYY",
              "version": "QQQ",
              "name": "ZZZ",
              "state": "activated enabled"
            }
          ]
        },
       
      ]
    }

"""

import jc.utils
import jc.parsers.universal
import re

class info():
    version = '1.0'
    description = '`systemextensionsctl list` command parser'
    author = 'Ron Green'
    author_email = '11993626+georgettica@users.noreply.github.com'
    compatible = ['darwin']
    magic_commands = ['systemextensionsctl list']

def parse(data, raw=False, quiet=False):
    """
    Parses the output of `systemextensionsctl list` command.

    Parameters:

        data:   (string)  Text data to parse

    Returns:

        Dictionary with parsed data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    if jc.utils.has_data(data):

        lines = data.strip().splitlines()
        total_extensions = None
        sections = []
        section = None
        headers = None

        line_iter = iter(lines)
        for line in line_iter:
            line = line.strip('\n')
            if line.endswith('extension(s)'):
                # Extract total_extensions
                match = re.match(r'(\d+)\s+extension\(s\)', line)
                if match:
                    total_extensions = int(match.group(1))
            elif line.startswith('--- '):
                # Start of a new section
                category_line = line
                # Extract category and description
                category_and_desc = line[4:]
                # Category is up to the first '('
                if '(' in category_and_desc:
                    category = category_and_desc.split('(')[0].strip()
                    description = category_and_desc[category_and_desc.find('(')+1:-1]
                else:
                    category = category_and_desc.strip()
                    description = ''
                section = {
                    'category': category,
                    'description': description,
                    'entries': []
                }
                sections.append(section)
                # Read the header line
                headers_line = next(line_iter)
                headers = headers_line.split('\t')
                # Normalize headers
                headers = [h.strip() for h in headers]
            else:
                # Data line
                if not line.strip():
                    continue
                fields = line.split('\t')
                # Pad fields with empty strings if needed
                if len(fields) < len(headers):
                    fields = fields + ['']*(len(headers) - len(fields))
                entry = {}
                for h, f in zip(headers, fields):
                    entry[h] = f.strip()
                # Optionally parse the 'bundleID (version)' field
                if 'bundleID (version)' in entry:
                    bundleID_version = entry['bundleID (version)']
                    match = re.match(r'(.+)\s+\((.+)\)', bundleID_version)
                    if match:
                        bundleID = match.group(1).strip()
                        version = match.group(2).strip()
                        entry['bundleID'] = bundleID
                        entry['version'] = version
                    else:
                        entry['bundleID'] = bundleID_version.strip()
                        entry['version'] = ''
                    del entry['bundleID (version)']
                # Optionally parse the '[state]' field
                if '[state]' in entry:
                    state = entry['[state]']
                    if state.startswith('[') and state.endswith(']'):
                        state_content = state[1:-1]
                        entry['state'] = state_content.strip()
                    else:
                        entry['state'] = state.strip()
                    del entry['[state]']
                # Add entry to the current section
                section['entries'].append(entry)

        result = {
            'total_extensions': total_extensions,
            'sections': sections
        }
        return result
    else:
        return {}
