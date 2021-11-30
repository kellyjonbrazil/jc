"""jc - JSON CLI output utility `ufw status` command output parser

Usage (cli):

    $ ufw status | jc --ufw

    or

    $ jc ufw status

Usage (module):

    import jc.parsers.ufw
    result = jc.parsers.ufw.parse(ufw_command_output)

Schema:

    {
      "status":                     string,
      "logging":                    string,
      "logging_level":              string,
      "default":                    string,
      "new_profiles":               string,
      "rules": [
        {
          "action":                 string,
          "action_direction":       string,     # null if blank
          "index":                  integer,    # null if blank
          "network_protocol":       string,
          "to_ip":                  string,
          "to_ip_prefix":           integer,
          "to_interface":           string,
          "to_transport":           string,
          "to_ports": [
                                    integer
          ],
          "to_port_ranges": [
            {
              "start":              integer,
              "end":                integer
            }
          ],
          "to_service":             string,     # null if any to ports or port_ranges are set
          "from_ip":                string,
          "from_ip_prefix":         integer,
          "from_interface":         string,
          "from_transport":         string,
          "from_ports": [
                                    integer
          ],
          "from_port_ranges": [
            {
              "start":              integer,
              "end":                integer
            }
          ],
          "from_service":           string,     # null if any from ports or port_ranges are set
          "comment":                string      # null if no comment
        }
      ]
    }

Examples:

    $ ufw status verbose | jc --ufw -p
    {
      "status": "active",
      "logging": "on",
      "logging_level": "low",
      "default": "deny (incoming), allow (outgoing), disabled (routed)",
      "new_profiles": "skip",
      "rules": [
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": null,
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": "any",
          "to_service": null,
          "to_ports": [
            22
          ],
          "to_ip": "0.0.0.0",
          "to_ip_prefix": 0,
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": 0,
          "from_interface": "any",
          "from_transport": "any",
          "from_port_ranges": [
            {
              "start": 0,
              "end": 65535
            }
          ],
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": null,
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": "tcp",
          "to_service": null,
          "to_ports": [
            80,
            443
          ],
          "to_ip": "0.0.0.0",
          "to_ip_prefix": 0,
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": 0,
          "from_interface": "any",
          "from_transport": "any",
          "from_port_ranges": [
            {
              "start": 0,
              "end": 65535
            }
          ],
          "from_service": null
        },
        ...
      ]
    }

    $ ufw status verbose | jc --ufw -p -r
    {
      "status": "active",
      "logging": "on",
      "logging_level": "low",
      "default": "deny (incoming), allow (outgoing), disabled (routed)",
      "new_profiles": "skip",
      "rules": [
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": null,
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": "any",
          "to_service": null,
          "to_ports": [
            "22"
          ],
          "to_ip": "0.0.0.0",
          "to_ip_prefix": "0",
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_port_ranges": [
            {
              "start": "0",
              "end": "65535"
            }
          ],
          "from_service": null
        },
        {
          "action": "ALLOW",
          "action_direction": "IN",
          "index": null,
          "network_protocol": "ipv4",
          "to_interface": "any",
          "to_transport": "tcp",
          "to_service": null,
          "to_ports": [
            "80",
            "443"
          ],
          "to_ip": "0.0.0.0",
          "to_ip_prefix": "0",
          "comment": null,
          "from_ip": "0.0.0.0",
          "from_ip_prefix": "0",
          "from_interface": "any",
          "from_transport": "any",
          "from_port_ranges": [
            {
              "start": "0",
              "end": "65535"
            }
          ],
          "from_service": null
        },
        ...
      ]
    }
"""
import jc.utils
import re
import ipaddress


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.1'
    description = '`ufw status` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['ufw status']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        Dictionary. Structured to conform to the schema.
    """
    int_list = ['index', 'to_ip_prefix', 'from_ip_prefix']

    if 'rules' in proc_data:
        for i, item in enumerate(proc_data['rules']):
            for key in item:
                if key in int_list:
                    proc_data['rules'][i][key] = jc.utils.convert_to_int(proc_data['rules'][i][key])

                if key in ['to_ports', 'from_ports']:
                    for i2, item2 in enumerate(proc_data['rules'][i][key]):
                        proc_data['rules'][i][key][i2] = jc.utils.convert_to_int(item2)

                if key in ['to_port_ranges', 'from_port_ranges']:
                    for i2, item2 in enumerate(proc_data['rules'][i][key]):
                        proc_data['rules'][i][key][i2]['start'] = jc.utils.convert_to_int(proc_data['rules'][i][key][i2]['start'])
                        proc_data['rules'][i][key][i2]['end'] = jc.utils.convert_to_int(proc_data['rules'][i][key][i2]['end'])

    return proc_data


def _parse_to_from(linedata, direction, rule_obj=None):

    if rule_obj is None:
        rule_obj = {}

    # pull out rule index, if they exist: [ 1]
    if direction == 'to':
        RE_LINE_NUM = re.compile(r'\[[ 0-9]+\]\s')
        line_number_match = re.search(RE_LINE_NUM, linedata)
        if line_number_match:
            rule_obj['index'] = line_number_match.group(0).replace('[', '').replace(']', '').strip()
            linedata = re.sub(RE_LINE_NUM, '', linedata)
        else:
            rule_obj['index'] = None

    # pull out comments, if they exist
    if direction == 'from':
        RE_COMMENT = re.compile(r'#.+$')
        comment_match = re.search(RE_COMMENT, linedata)
        if comment_match:
            rule_obj['comment'] = comment_match.group(0).lstrip('#').strip()
            linedata = re.sub(RE_COMMENT, '', linedata)
        else:
            rule_obj['comment'] = None

    # pull (v6)
    RE_V6 = re.compile(r'\(v6\)')
    v6_match = re.search(RE_V6, linedata)
    if v6_match:
        rule_obj['network_protocol'] = 'ipv6'
        linedata = re.sub(RE_V6, '', linedata)
    elif not rule_obj.get('network_protocol'):
        rule_obj['network_protocol'] = 'ipv4'

    # pull 'Anywhere' if exists. Assign to 0.0.0.0/0 or ::/0 depending on if (v6) is found
    if 'Anywhere' in linedata:
        if rule_obj.get('network_protocol') == 'ipv6':
            rule_obj[direction + '_ip'] = '::'
            rule_obj[direction + '_ip_prefix'] = '0'
        elif rule_obj.get('network_protocol') == 'ipv4':
            rule_obj[direction + '_ip'] = '0.0.0.0'
            rule_obj[direction + '_ip_prefix'] = '0'
        linedata = linedata.replace('Anywhere', '')

    # pull out interface (after 'on')
    linedata_list = linedata.split(' on ', maxsplit=1)

    if len(linedata_list) > 1:
        rule_obj[direction + '_interface'] = linedata_list[1].strip()
        linedata = linedata_list[0]
    else:
        rule_obj[direction + '_interface'] = 'any'

    # pull tcp/udp/etc. transport - strip on '/'
    linedata_list = linedata.rsplit('/', maxsplit=1)
    if len(linedata_list) > 1:
        if linedata_list[1].strip() in ['tcp', 'udp', 'ah', 'esp', 'gre', 'ipv6', 'igmp']:
            rule_obj[direction + '_transport'] = linedata_list[1].strip()
            linedata = linedata_list[0]
        else:
            rule_obj[direction + '_transport'] = 'any'
    else:
        rule_obj[direction + '_transport'] = 'any'

    # pull out ipv4 or ipv6 addresses
    linedata_list = linedata.split()
    new_linedata_list = []

    valid_ip = None
    for item in linedata_list:
        try:
            valid_ip = ipaddress.IPv4Interface(item)
        except Exception:
            try:
                valid_ip = ipaddress.IPv6Interface(item)
            except Exception:
                new_linedata_list.append(item)

    if valid_ip:
        rule_obj[direction + '_ip'] = str(valid_ip.ip)
        rule_obj[direction + '_ip_prefix'] = str(valid_ip.with_prefixlen.split('/')[1])
        linedata = ' '.join(new_linedata_list)

    # find the numeric port(s)
    linedata_list = linedata.split(',')
    port_list = []
    port_ranges = []
    for item in linedata_list:
        if item.strip().isnumeric():
            port_list.append(item.strip())
        elif ':' in item:
            p_range = item.strip().split(':', maxsplit=1)
            port_ranges.append(
                {
                    "start": p_range[0],
                    "end": p_range[1]
                }
            )

    if port_list or port_ranges:
        rule_obj[direction + '_service'] = None
        linedata = ''

    if port_list:
        rule_obj[direction + '_ports'] = port_list

    if port_ranges:
        rule_obj[direction + '_port_ranges'] = port_ranges

    # only thing left should be the service name.
    if linedata.strip():
        rule_obj[direction + '_service'] = linedata.strip()
        rule_obj[direction + '_transport'] = None

    # check if to/from IP addresses exist. If not, set to 0.0.0.0/0 or ::/0
    if direction + '_ip' not in rule_obj:
        if rule_obj.get('network_protocol') == 'ipv6':
            rule_obj[direction + '_ip'] = '::'
            rule_obj[direction + '_ip_prefix'] = '0'
        elif rule_obj.get('network_protocol') == 'ipv4':
            rule_obj[direction + '_ip'] = '0.0.0.0'
            rule_obj[direction + '_ip_prefix'] = '0'

    # finally set default ports if no ports exist and there should be some
    if direction + '_transport' in rule_obj:
        if rule_obj[direction + '_transport'] in ['tcp', 'udp', 'any']:
            if not port_list and not port_ranges:
                rule_obj[direction + '_port_ranges'] = [
                    {
                        'start': '0',
                        'end': '65535'
                    }
                ]
                rule_obj[direction + '_service'] = None

    return rule_obj


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}
    rules_list = []

    if jc.utils.has_data(data):

        rule_lines = False

        for line in filter(None, data.splitlines()):

            if line.startswith('Status: '):
                raw_output['status'] = line.split(': ', maxsplit=1)[1]
                continue

            if line.startswith('Logging: '):
                log_line = line.split(': ', maxsplit=1)
                log_line = log_line[1]
                log_line = log_line.split()
                raw_output['logging'] = log_line[0]
                if len(log_line) == 2:
                    raw_output['logging_level'] = log_line[1].replace('(', '').replace(')', '').strip()
                continue

            if line.startswith('Default: '):
                raw_output['default'] = line.split(': ', maxsplit=1)[1]
                continue

            if line.startswith('New profiles: '):
                raw_output['new_profiles'] = line.split(': ', maxsplit=1)[1]
                continue

            if 'To' in line and 'Action' in line and 'From' in line:
                rule_lines = True
                continue

            if rule_lines:
                if '------' in line:
                    continue

                # Split on action. Left of Action is 'to', right of Action is 'from'
                rule_obj = {}

                splitline = re.split(r'(ALLOW IN|ALLOW OUT|ALLOW FWD|DENY IN|DENY OUT|DENY FWD|LIMIT IN|LIMIT OUT|LIMIT FWD|REJECT IN|REJECT OUT|REJECT FWD|ALLOW|DENY|LIMIT|REJECT)', line)
                to_line = splitline[0]
                action_line = splitline[1]
                action_list = action_line.split()
                from_line = splitline[2]
                action_direction = None

                if len(action_list) == 1:
                    action = action_list[0]
                elif len(action_list) == 2:
                    action = action_list[0]
                    action_direction = action_list[1]

                rule_obj['action'] = action
                rule_obj['action_direction'] = action_direction
                rule_obj.update(_parse_to_from(to_line, 'to'))
                rule_obj.update(_parse_to_from(from_line, 'from', rule_obj))

                rules_list.append(rule_obj)

        raw_output['rules'] = rules_list

    if raw:
        return raw_output
    else:
        return _process(raw_output)
