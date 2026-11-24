r"""jc - JSON Convert `id` command output parser

Usage (cli):

    $ id | jc --id

or

    $ jc id

Usage (module):

    import jc
    result = jc.parse('id', id_command_output)

Schema:

    {
      "uid": {
        "id":       integer,
        "name":     string
      },
      "gid": {
        "id":       integer,
        "name":     string
      },
      "groups": [
        {
          "id":     integer,
          "name":   string
        },
        {
          "id":     integer,
          "name":   string
        }
      ],
      "context": {
        "user":     string,
        "role":     string,
        "type":     string,
        "level":    string
      }
    }

Examples:

    $ id | jc --id -p
    {
      "uid": {
        "id": 1000,
        "name": "joeuser"
      },
      "gid": {
        "id": 1000,
        "name": "joeuser"
      },
      "groups": [
        {
          "id": 1000,
          "name": "joeuser"
        },
        {
          "id": 10,
          "name": "wheel"
        }
      ],
      "context": {
        "user": "unconfined_u",
        "role": "unconfined_r",
        "type": "unconfined_t",
        "level": "s0-s0:c0.c1023"
      }
    }

    $ id | jc --id -p -r
    {
      "uid": {
        "id": "1000",
        "name": "joeuser"
      },
      "gid": {
        "id": "1000",
        "name": "joeuser"
      },
      "groups": [
        {
          "id": "1000",
          "name": "joeuser"
        },
        {
          "id": "10",
          "name": "wheel"
        }
      ],
      "context": {
        "user": "unconfined_u",
        "role": "unconfined_r",
        "type": "unconfined_t",
        "level": "s0-s0:c0.c1023"
      }
    }
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.8'
    description = '`id` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'aix', 'freebsd']
    magic_commands = ['id']
    tags = ['command', 'slurpable']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    if 'uid' in proc_data:
        if 'id' in proc_data['uid']:
            proc_data['uid']['id'] = jc.utils.convert_to_int(proc_data['uid']['id'])

    if 'gid' in proc_data:
        if 'id' in proc_data['gid']:
            proc_data['gid']['id'] = jc.utils.convert_to_int(proc_data['gid']['id'])

    if 'groups' in proc_data:
        for group in proc_data['groups']:
            if 'id' in group:
                group['id'] = jc.utils.convert_to_int(group['id'])

    return proc_data


# fields in the order `id` prints them. euid and egid are skipped.
_FIELDS = ('uid', 'gid', 'euid', 'egid', 'groups', 'context')


def _find_key(data, pos, keys):
    """
    Find the first 'key=' (for any of keys) at or after pos that is at the
    start of the string or follows a space. Returns (index, key) or
    (-1, None) if not found.
    """
    found = (-1, None)

    for key in keys:
        idx = data.find(key + '=', pos)
        while idx != -1 and idx > 0 and data[idx - 1] != ' ':
            idx = data.find(key + '=', idx + 1)

        if idx != -1 and (found[0] == -1 or idx < found[0]):
            found = (idx, key)

    return found


def _name_ends(data, pos, keys, comma):
    """
    True if a name that closes with ')' at pos - 1 ends here: at the end of
    the string, before a ',' (if comma is True), or before blanks followed
    by one of the 'key=' strings.
    """
    if pos == len(data) or (comma and data[pos] == ','):
        return True

    blank_end = pos
    while blank_end < len(data) and data[blank_end] == ' ':
        blank_end += 1

    if blank_end == pos:
        return False

    if blank_end == len(data):
        return True

    return any(data.startswith(key + '=', blank_end) for key in keys)


def _id_name(data, pos, keys, comma=False):
    """
    Parse 'N' or 'N(name)' starting at pos. The name may contain any text up
    to the ')' that ends the item (see _name_ends). Returns (id, name, end).
    """
    stop_chars = '(, ' if comma else '( '
    end = pos
    while end < len(data) and data[end] not in stop_chars:
        end += 1

    item_id = data[pos:end]

    if end == len(data) or data[end] != '(':
        return item_id, None, end

    close = data.find(')', end + 1)
    while close != -1 and not _name_ends(data, close + 1, keys, comma):
        close = data.find(')', close + 1)

    if close == -1:
        # no closing parenthesis: the name is the rest of the item
        name_end = end + 1
        while name_end < len(data) and data[name_end] not in stop_chars[1:]:
            name_end += 1
        return item_id, data[end + 1:name_end], name_end

    return item_id, data[end + 1:close], close + 1


def parse(data, raw=False, quiet=False):
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

    raw_output = {}

    if jc.utils.has_data(data):
        data = data.strip()
        remaining = _FIELDS
        pos, key = _find_key(data, 0, ('uid', 'gid', 'groups', 'context'))

        while key:
            remaining = remaining[remaining.index(key) + 1:]
            pos += len(key) + 1

            if key == 'context':
                context_parsed = data[pos:].split(':', maxsplit=3)
                raw_output['context'] = {}
                raw_output['context']['user'] = context_parsed[0]
                raw_output['context']['role'] = context_parsed[1]
                raw_output['context']['type'] = context_parsed[2]
                raw_output['context']['level'] = context_parsed[3]
                break

            if key == 'groups':
                raw_output['groups'] = []
                while True:
                    group_id, group_name, pos = _id_name(data, pos, remaining, comma=True)
                    raw_output['groups'].append({'id': group_id, 'name': group_name})
                    if pos < len(data) and data[pos] == ',':
                        pos += 1
                        continue
                    break

            else:
                item_id, item_name, pos = _id_name(data, pos, remaining)
                if key in ('uid', 'gid'):
                    raw_output[key] = {'id': item_id, 'name': item_name}

            pos, key = _find_key(data, pos, remaining)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
