r"""jc - JSON Convert `lspci -mmv` command output parser

This parser supports the following `lspci` options:
- `-mmv`
- `-nmmv`
- `-nnmmv`
- `-vvvnn`

Usage (cli):

    $ lspci -nnmmv | jc --lspci

or

    $ jc lspci -nnmmv

Usage (module):

    import jc
    result = jc.parse('lspci', lspci_command_output)

Schema:

    [
      {
        "slot":                         string,
        "domain":                       string,
        "domain_int":                   integer,
        "bus":                          string,
        "bus_int":                      integer,
        "dev":                          string,
        "dev_int":                      integer,
        "function":                     string,
        "function_int":                 integer,
        "class":                        string,
        "class_id":                     string,
        "class_id_int":                 integer,
        "vendor":                       string,
        "vendor_id":                    string,
        "vendor_id_int":                integer,
        "device":                       string,
        "device_id":                    string,
        "device_id_int":                integer,
        "svendor":                      string,
        "svendor_id":                   string,
        "svendor_id_int":               integer,
        "sdevice":                      string,
        "sdevice_id":                   string,
        "sdevice_id_int":               integer,
        "rev":                          string,
        "physlot":                      string,
        "progif":                       string,
        "progif_int":                   integer
      }
    ]

Verbose (`-vvvnn`) Schema:

    Source-derived keys keep the exact `lspci` spelling. Parser-created
    keys are PascalCase. All values are strings except `Offset` and
    `Version`, which are null when not printed. Sections that cannot be
    parsed are returned as {"Raw": string}.

    [
      {
        "Slot":                         string,
        "Class":                        string,
        "ClassId":                      string,
        "Description":                  string,
        "VendorId":                     string,
        "DeviceId":                     string,
        "Rev":                          string,
        "ProgIf":                       string,
        "ProgIfName":                   string,
        "Subsystem": {
          "Description":                string,
          "VendorId":                   string,
          "DeviceId":                   string
        },
        "<Label>":                      string or object,
        "Regions": [
          {
            "Index":                    string,
            "Type":                     string,
            "Address":                  string,
            "Width":                    string,
            "Prefetchability":          string,
            "Size":                     string,
            "Attributes": [
                                        string
            ]
          }
        ],
        "Capabilities": [
          {
            "Offset":                   string/null,
            "Version":                  string/null,
            "Description":              string,
            "<Label>":                  string or object
          }
        ],
        "Raw":                          string
      }
    ]

Examples:

    $ lspci -nnmmv | jc --lspci -p
    [
      {
        "slot": "ff:02:05.0",
        "domain": "ff",
        "domain_int": 255,
        "bus": "02",
        "bus_int": 2,
        "dev": "05",
        "dev_int": 5,
        "function": "0",
        "function_int": 0,
        "class": "SATA controller",
        "class_id": "0106",
        "class_id_int": 262,
        "vendor": "VMware",
        "vendor_id": "15ad",
        "vendor_id_int": 5549,
        "device": "SATA AHCI controller",
        "device_id": "07e0",
        "device_id_int": 2016,
        "svendor": "VMware",
        "svendor_id": "15ad",
        "svendor_id_int": 5549,
        "sdevice": "SATA AHCI controller",
        "sdevice_id": "07e0",
        "sdevice_id_int": 2016,
        "physlot": "37",
        "progif": "01",
        "progif_int": 1
      },
      ...
    ]

    $ lspci -nnmmv | jc --lspci -p -r
    [
      {
        "slot": "ff:02:05.0",
        "domain": "ff",
        "bus": "02",
        "dev": "05",
        "function": "0",
        "class": "SATA controller",
        "class_id": "0106",
        "vendor": "VMware",
        "vendor_id": "15ad",
        "device": "SATA AHCI controller",
        "device_id": "07e0",
        "svendor": "VMware",
        "svendor_id": "15ad",
        "sdevice": "SATA AHCI controller",
        "sdevice_id": "07e0",
        "physlot": "37",
        "progif": "01"
      },
      ...
    ]
"""
import re
from typing import List, Dict, Set, Optional, Tuple
from jc.jc_types import JSONDictType
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.2'
    description = '`lspci -mmv` and `lspci -vvvnn` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    magic_commands = ['lspci']
    tags = ['command']


__version__ = info.version


_SLOT = r'(?:[0-9a-f]{4,}:)?[0-9a-f]{2}:[0-9a-f]{2}\.[0-7]'
_V_DETECT_RE = re.compile(r'^' + _SLOT + r' ')
_V_HEADER_RE = re.compile(
    r'^(?P<Slot>' + _SLOT + r') (?P<Class>.+?) \[(?P<ClassId>[0-9a-f]{4})\]: '
    r'(?P<Description>.+?) \[(?P<VendorId>[0-9a-f]{4}):(?P<DeviceId>[0-9a-f]{4})\]'
    r'(?: \(rev (?P<Rev>[0-9a-f]{2})\))?'
    r'(?: \(prog-if (?P<ProgIf>[0-9a-f]{2})(?: \[(?P<ProgIfName>[^\]]*)\])?\))?$'
)
_V_CAP_RE = re.compile(
    r'^Capabilities: (?:\[(?P<Offset>[0-9a-f]+)(?: v(?P<Version>\d+))?\] )?(?P<Description>.*)$'
)
_V_REGION_RE = re.compile(
    r'^Region (?P<Index>\d+): (?P<Type>Memory|I/O ports) at (?P<Address>\S+)'
    r'(?: \((?P<Width>[^,()]+), (?P<Prefetchability>[^)]+)\))?(?P<Rest>(?: \[[^\]]*\])*)$'
)
_V_ROM_RE = re.compile(r'^Expansion ROM at (?P<Address>\S+)(?P<Rest>(?: \[[^\]]*\])*)$')
_V_BRACKET_RE = re.compile(r'\[([^\]]*)\]')
_V_SUBSYS_RE = re.compile(
    r'^(?P<Description>.*) \[(?P<VendorId>[0-9a-f]{4}):(?P<DeviceId>[0-9a-f]{4})\]$'
)
_V_LABEL_RE = re.compile(r'^([^\s:][^:\t]*?):(?:[\t ]+(.*))?$')
_V_CONTAINER_RE = re.compile(r'^[^\s:]+:\t')
_V_MULTI_LABEL_SPLIT_RE = re.compile(r' {2,}(?=[A-Za-z][\w ]*: )')
_V_FLAG_RE = re.compile(r'^(\S*[^\s+\-=])([+-])$')
_V_KV_RE = re.compile(r'^([^\s=]+)=(\S*)$')
_V_GROUP_RE = re.compile(r'^([^\s(]+)\((.*)\)$')
_V_PM_STATE_RE = re.compile(r'^(D\d\S*)(?:\s+(.*))?$')
_V_INLINE_CAP_RE = re.compile(
    r'^(?:MSI|MSI-X|Vendor Specific Information|Designated Vendor-Specific): (.*?)(?: <\?>)?$'
)

_V_EOL_LABELS = ('Compliance Preset/De-emphasis',)
_V_LATENCY_KEYS = ('L0s', 'L1')
_V_WORD_VALUE_KEYS = {
    'MaxPayload', 'PhantFunc', 'SlotPowerLimit', 'MaxReadReq', 'Port', 'Speed',
    'Width', 'ASPM', 'RCB', 'OBFF', 'EmergencyPowerReduction', 'Slot', 'PowerLimit',
    'IntMsgNum', 'AttnInd', 'PwrInd', 'MaxGroups', 'WindowSz', 'NumGroups',
    'IndexPos', 'BaseAddr', 'OverlaySize', 'MaxEETLPPrefixes'
}
_V_DEVICE_TOKEN_FIELDS = {'Control', 'Status', 'Secondary status', 'BridgeCtl', 'Bus'}
_V_RESERVED_CAP_KEYS = {'Offset', 'Version', 'Description', 'Raw'}


class _ParseError(Exception):
    pass


def _v_collapse(text: str) -> str:
    return ' '.join(text.split())


def _v_put(obj: Dict, key: str, value) -> None:
    if key in obj:
        raise _ParseError(f'duplicate key: {key}')
    obj[key] = value


def _v_is_structured(token: str) -> bool:
    return bool(_V_FLAG_RE.match(token) or _V_KV_RE.match(token) or _V_GROUP_RE.match(token))


def _v_put_token(obj: Dict, token: str) -> None:
    m = _V_GROUP_RE.match(token)
    if m:
        group: Dict = {}
        for item in filter(None, (i.strip() for i in m.group(2).split(','))):
            _v_put_token(group, item)
        _v_put(obj, m.group(1), group)
        return

    m = _V_FLAG_RE.match(token)
    if m:
        _v_put(obj, m.group(1), m.group(2))
        return

    m = _V_KV_RE.match(token)
    if m:
        _v_put(obj, m.group(1), m.group(2))
        return

    raise _ParseError(f'unknown token: {token}')


def _v_split_segments(text: str) -> List[str]:
    segments: List[str] = []
    buf: List[str] = []
    depth = 0
    for ch in text:
        if ch in '([':
            depth += 1
        elif ch in ')]' and depth:
            depth -= 1

        if ch in ',;' and depth == 0:
            segments.append(''.join(buf))
            buf = []
        else:
            buf.append(ch)

    segments.append(''.join(buf))
    return [s.strip() for s in segments if s.strip()]


def _v_label_value(rest: List[str]):
    if rest and all(_v_is_structured(t) for t in rest):
        obj: Dict = {}
        for token in rest:
            _v_put_token(obj, token)
        return obj
    return ' '.join(rest)


def _v_parse_segment(segment: str, obj: Dict, state: Dict) -> None:
    tokens = segment.split()

    if tokens[0] in _V_LATENCY_KEYS and state.get('latency') is not None:
        if len(tokens) < 2:
            raise _ParseError('missing latency value')
        _v_put(state['latency'], tokens[0], ' '.join(tokens[1:]))
        return
    state['latency'] = None

    pending: List[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.endswith(':') and len(token) > 1:
            label = ' '.join(pending + [token[:-1]])
            _v_put(obj, label, _v_label_value(tokens[i + 1:]))
            return

        if pending:
            if _v_is_structured(token):
                raise _ParseError(f'orphan words: {pending}')
            pending.append(token)
            i += 1
            continue

        latency_key = None
        if token == 'Latency':
            latency_key, start = 'Latency', i + 1
        elif token == 'Exit' and i + 1 < len(tokens) and tokens[i + 1] == 'Latency':
            latency_key, start = 'Exit Latency', i + 2

        if latency_key:
            if start + 1 >= len(tokens) or tokens[start] not in _V_LATENCY_KEYS:
                raise _ParseError('malformed latency')
            latency: Dict = {tokens[start]: ' '.join(tokens[start + 1:])}
            _v_put(obj, latency_key, latency)
            state['latency'] = latency
            return

        if _v_is_structured(token):
            _v_put_token(obj, token)
            i += 1
            continue

        if token in _V_WORD_VALUE_KEYS:
            j = i + 1
            while j < len(tokens) and not (
                _v_is_structured(tokens[j])
                or tokens[j] in _V_WORD_VALUE_KEYS
                or tokens[j].endswith(':')
            ):
                j += 1
            if j == i + 1:
                raise _ParseError(f'missing value for {token}')
            _v_put(obj, token, ' '.join(tokens[i + 1:j]))
            i = j
            continue

        pending.append(token)
        i += 1

    if pending:
        raise _ParseError(f'orphan words: {pending}')


def _v_parse_line(line: str, obj: Dict, state: Dict) -> None:
    for label in _V_EOL_LABELS:
        idx = line.find(label + ': ')
        if idx != -1 and (idx == 0 or line[idx - 1] == ' '):
            prefix = line[:idx].strip()
            if prefix:
                _v_parse_line(prefix, obj, state)
            _v_put(obj, label, line[idx + len(label) + 2:].strip())
            return

    for segment in _v_split_segments(line):
        _v_parse_segment(segment, obj, state)


def _v_is_free_text(text: str) -> bool:
    return not any(_v_is_structured(t) or t.endswith(':') for t in text.split())


def _v_section_value(lines: List[str]):
    lines = [line.strip() for line in lines if line.strip()]
    if not lines:
        return {}

    obj: Dict = {}
    try:
        for line in lines:
            _v_parse_line(line, obj, {'latency': None})
        return obj
    except _ParseError:
        text = _v_collapse(' '.join(lines))
        if _v_is_free_text(text):
            return text
        raise


def _v_split_labels(text: str) -> List[str]:
    parts = _V_MULTI_LABEL_SPLIT_RE.split(text)
    if len(parts) > 1:
        matches = [_V_LABEL_RE.match(p) for p in parts]
        if all(m and m.group(2) for m in matches):
            return parts
    return [text]


def _v_sections(lines: List[Tuple[int, bool, str]], base: int):
    sections: List[List] = []
    raw: List[str] = []
    current = None
    for depth, extra, text in lines:
        if depth <= base and not extra:
            for part in _v_split_labels(text):
                m = _V_LABEL_RE.match(part)
                if m:
                    current = [m.group(1), m.group(2) or '', []]
                    sections.append(current)
                else:
                    raw.append(part)
                    current = None
        elif current is not None:
            current[2].append((depth, extra, text))
        else:
            raw.append(text)
    return sections, raw


def _v_section_raw(label: str, inline: str, children: List[Tuple[int, bool, str]]) -> Dict:
    text = ' '.join([f'{label}: {inline}'] + [t for _, _, t in children])
    return {'Raw': _v_collapse(text)}


def _v_build_section(label: str, inline: str, children: List[Tuple[int, bool, str]],
                     base: int, cap_desc: str):
    is_container = bool(inline and _V_CONTAINER_RE.match(inline)) or (
        not inline and bool(children)
        and children[0][0] == base + 1 and not children[0][1]
        and bool(_V_LABEL_RE.match(children[0][2]))
    )

    if is_container:
        sub_lines = ([(base + 1, False, inline)] if inline else []) + children
        subs, raw = _v_sections(sub_lines, base + 1)
        obj: Dict = {}
        for sub_label, sub_inline, sub_children in subs:
            try:
                value = _v_build_section(sub_label, sub_inline, sub_children, base + 1, cap_desc)
            except _ParseError:
                value = _v_section_raw(sub_label, sub_inline, sub_children)
            if sub_label in obj:
                raw.append(_v_section_raw(sub_label, sub_inline, sub_children)['Raw'])
            else:
                obj[sub_label] = value
        if raw:
            _v_put(obj, 'Raw', _v_collapse(' '.join(raw)))
        return obj

    lines = [inline] + [t for _, _, t in children]

    if label == 'Status' and cap_desc.startswith('Power Management'):
        m = _V_PM_STATE_RE.match(lines[0].strip())
        if m:
            rest = _v_section_value([m.group(2) or ''] + lines[1:])
            if not isinstance(rest, dict):
                raise _ParseError('unexpected power management status')
            obj = {'State': m.group(1)}
            for k, v in rest.items():
                _v_put(obj, k, v)
            return obj

    return _v_section_value(lines)


def _v_capability(head: str, body: List[Tuple[int, bool, str]]) -> Dict:
    m = _V_CAP_RE.match(head)
    if m:
        cap: Dict = m.groupdict()
    else:
        cap = {'Offset': None, 'Version': None, 'Description': head}

    raw: List[str] = []
    desc = cap['Description']

    m = _V_INLINE_CAP_RE.match(desc)
    if m:
        inline: Dict = {}
        try:
            _v_parse_line(m.group(1), inline, {'latency': None})
            for k, v in inline.items():
                _v_put(cap, k, v)
        except _ParseError:
            pass

    sections, unlabeled = _v_sections(body, 2)
    raw.extend(unlabeled)

    for label, inline_text, children in sections:
        try:
            value = _v_build_section(label, inline_text, children, 2, desc)
        except _ParseError:
            value = _v_section_raw(label, inline_text, children)

        if label in cap or label in _V_RESERVED_CAP_KEYS:
            raw.append(_v_section_raw(label, inline_text, children)['Raw'])
        else:
            cap[label] = value

    if raw:
        cap['Raw'] = _v_collapse(' '.join(raw))

    return cap


def _v_bracket_fields(rest: str, obj: Dict) -> None:
    attributes: List[str] = []
    for item in _V_BRACKET_RE.findall(rest):
        if item.startswith('size='):
            obj['Size'] = item[5:]
        else:
            attributes.append(item)
    obj['Attributes'] = attributes


def _v_device_field(dev: Dict, head: str, body: List[Tuple[int, bool, str]], raw: List[str]) -> None:
    continuation = [t for _, _, t in body]
    full_text = _v_collapse(' '.join([head] + continuation))

    m = _V_REGION_RE.match(head)
    if m and not continuation:
        region = {k: v for k, v in m.groupdict().items() if k != 'Rest' and v is not None}
        _v_bracket_fields(m.group('Rest'), region)
        dev.setdefault('Regions', []).append(region)
        return

    m = _V_ROM_RE.match(head)
    if m and not continuation:
        rom = {'Address': m.group('Address')}
        _v_bracket_fields(m.group('Rest'), rom)
        if 'Expansion ROM' in dev:
            raw.append(full_text)
        else:
            dev['Expansion ROM'] = rom
        return

    m = _V_LABEL_RE.match(head)
    if not m:
        raw.append(full_text)
        return

    label, value = m.group(1), m.group(2) or ''
    if label in dev:
        raw.append(full_text)
        return

    try:
        if label == 'Subsystem' and not continuation:
            sm = _V_SUBSYS_RE.match(value)
            dev[label] = sm.groupdict() if sm else {'Description': value}
        elif label in _V_DEVICE_TOKEN_FIELDS:
            dev[label] = _v_section_value([value] + continuation)
        elif label == 'Latency' and not continuation and ', Cache Line Size: ' in value:
            latency, cache_line = value.split(', Cache Line Size: ', 1)
            dev[label] = latency
            if 'Cache Line Size' in dev:
                raise _ParseError('duplicate key: Cache Line Size')
            dev['Cache Line Size'] = cache_line
        else:
            dev[label] = ' '.join([value] + continuation).strip()
    except _ParseError:
        dev[label] = {'Raw': full_text}


def _v_device(header: Optional[str], blocks: List) -> Dict:
    dev: Dict = {}
    raw: List[str] = []

    if header is not None:
        m = _V_HEADER_RE.match(header)
        if m:
            dev = {k: v for k, v in m.groupdict().items() if v is not None}
        else:
            raw.append(header)

    for head, body in blocks:
        if head.startswith('Capabilities:'):
            dev.setdefault('Capabilities', []).append(_v_capability(head, body))
        else:
            _v_device_field(dev, head, body, raw)

    if raw:
        dev['Raw'] = _v_collapse(' '.join(raw))

    return dev


def _parse_verbose(data: str) -> List[JSONDictType]:
    devices: List[Dict] = []
    current: Optional[Dict] = None

    for line in data.splitlines():
        if not line.strip():
            current = None
            continue

        depth = len(line) - len(line.lstrip('\t'))
        rest = line[depth:]
        extra = rest.startswith(' ')
        text = rest.strip()

        if depth == 0 and not extra:
            current = {'header': text, 'blocks': []}
            devices.append(current)
            continue

        if current is None:
            current = {'header': None, 'blocks': []}
            devices.append(current)

        if depth == 1 and not extra or not current['blocks']:
            current['blocks'].append((text, []))
        else:
            current['blocks'][-1][1].append((depth, extra, text))

    return [_v_device(d['header'], d['blocks']) for d in devices]


def _process(proc_data: List[JSONDictType]) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    int_list: Set[str] = {
        'domain', 'bus', 'dev', 'function', 'class_id', 'vendor_id', 'device_id',
        'svendor_id', 'sdevice_id', 'progif'
    }

    new_list: List[JSONDictType] = []

    for item in proc_data:
        output: Dict = {}
        for key, val in item.items():
            output[key] = val
            if key in int_list:
                output[key + '_int'] = int(val, 16)
        new_list.append(output)

    return new_list


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List = []
    device_output: Dict = {}

    if jc.utils.has_data(data):
        first_line = next(line for line in data.splitlines() if line.strip())
        if _V_DETECT_RE.match(first_line):
            return _parse_verbose(data)

        item_id_p = re.compile(r'(?P<id>^[0-9a-f]{4}$)')
        item_id_bracket_p = re.compile(r' \[(?P<id>[0-9a-f]{4})\]$')

        for line in filter(None, data.splitlines()):
            if line.startswith('Slot:'):
                if device_output:
                    raw_output.append(device_output)
                    device_output = {}

                device_output['slot'] = line.split()[1]

                slot_info = line.split()[1]
                *domain, bus, dev_fun = slot_info.split(':')

                if domain:
                    dom = domain[0]
                else:
                    dom = "00"

                dev, fun = dev_fun.split('.')
                device_output['domain'] = dom
                device_output['bus'] = bus
                device_output['dev'] = dev
                device_output['function'] = fun
                continue

            key, val = line.split(maxsplit=1)
            key = key[:-1].lower()

            # numeric only (-nmmv)
            if item_id_p.match(val):
                device_output[key + '_id'] = val
                continue

            # string and numeric (-nnmmv)
            if item_id_bracket_p.search(val):
                string, idnum = val.rsplit(maxsplit=1)
                device_output[key] = string
                device_output[key + '_id'] = idnum[1:-1]
                continue

            # string only (-mmv)
            device_output[key] = val
            continue


        if device_output:
            raw_output.append(device_output)

    return raw_output if raw else _process(raw_output)
