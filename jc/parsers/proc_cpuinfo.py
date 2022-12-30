"""jc - JSON Convert `/proc/cpuinfo` file parser

Usage (cli):

    $ cat /proc/cpuinfo | jc --proc

or

    $ jc /proc/cpuinfo

or

    $ cat /proc/cpuinfo | jc --proc-cpuinfo

Usage (module):

    import jc
    result = jc.parse('proc', proc_cpuinfo_file)

or

    import jc
    result = jc.parse('proc_cpuinfo', proc_cpuinfo_file)

Schema:

Integer, float, and boolean ("yes"/"no") conversions are attempted. Blank
strings are converted to `null`.

"Well-known" keys like `cache size`, `address types`, `bugs`, and `flags`
are processed into sensible data types. (see below)

If this is not desired, then use the `--raw` (CLI) or `raw=True` (Module)
option.

    [
      {
        "processor":                  integer,
        "address sizes":              string,
        "address_size_physical":      integer,  # in bits
        "address_size_virtual":       integer,  # in bits
        "cache size":                 string,
        "cache_size_num":             integer,
        "cache_size_unit":            string,
        "flags": [
                                      string
        ],
        "bugs": [
                                      string
        ],
        "bogomips":                   float,
        <key>:                        string/int/float/boolean/null
      }
    ]

Examples:

    $ cat /proc/cpuinfo | jc --proc -p
    [
      {
        "processor": 0,
        "vendor_id": "GenuineIntel",
        "cpu family": 6,
        "model": 142,
        "model name": "Intel(R) Core(TM) i5-8279U CPU @ 2.40GHz",
        "stepping": 10,
        "cpu MHz": 2400.0,
        "cache size": "6144 KB",
        "physical id": 0,
        "siblings": 1,
        "core id": 0,
        "cpu cores": 1,
        "apicid": 0,
        "initial apicid": 0,
        "fpu": true,
        "fpu_exception": true,
        "cpuid level": 22,
        "wp": true,
        "bogomips": 4800.0,
        "clflush size": 64,
        "cache_alignment": 64,
        "address sizes": "45 bits physical, 48 bits virtual",
        "power management": null,
        "address_size_physical": 45,
        "address_size_virtual": 48,
        "cache_size_num": 6144,
        "cache_size_unit": "KB",
        "flags": [
          "fpu",
          "vme",
          "de",
          "pse",
          "tsc",
          "msr",
          "pae",
          "mce",
          "cx8",
          "apic",
          "sep",
          "mtrr",
          "pge",
          "mca",
          "cmov",
          "pat",
          "pse36",
          "clflush",
          "mmx",
          "fxsr",
          "sse",
          "sse2",
          "ss",
          "syscall",
          "nx",
          "pdpe1gb",
          "rdtscp",
          "lm",
          "constant_tsc",
          "arch_perfmon",
          "nopl",
          "xtopology",
          "tsc_reliable",
          "nonstop_tsc",
          "cpuid",
          "pni",
          "pclmulqdq",
          "ssse3",
          "fma",
          "cx16",
          "pcid",
          "sse4_1",
          "sse4_2",
          "x2apic",
          "movbe",
          "popcnt",
          "tsc_deadline_timer",
          "aes",
          "xsave",
          "avx",
          "f16c",
          "rdrand",
          "hypervisor",
          "lahf_lm",
          "abm",
          "3dnowprefetch",
          "cpuid_fault",
          "invpcid_single",
          "pti",
          "ssbd",
          "ibrs",
          "ibpb",
          "stibp",
          "fsgsbase",
          "tsc_adjust",
          "bmi1",
          "avx2",
          "smep",
          "bmi2",
          "invpcid",
          "rdseed",
          "adx",
          "smap",
          "clflushopt",
          "xsaveopt",
          "xsavec",
          "xgetbv1",
          "xsaves",
          "arat",
          "md_clear",
          "flush_l1d",
          "arch_capabilities"
        ],
        "bugs": [
          "cpu_meltdown",
          "spectre_v1",
          "spectre_v2",
          "spec_store_bypass",
          "l1tf",
          "mds",
          "swapgs",
          "itlb_multihit",
          "srbds"
        ]
      },
      ...
    ]

    $ cat /proc/cpuinfo | jc --proc_cpuinfo -p -r
    [
      {
        "processor": "0",
        "vendor_id": "GenuineIntel",
        "cpu family": "6",
        "model": "142",
        "model name": "Intel(R) Core(TM) i5-8279U CPU @ 2.40GHz",
        "stepping": "10",
        "cpu MHz": "2400.000",
        "cache size": "6144 KB",
        "physical id": "0",
        "siblings": "1",
        "core id": "0",
        "cpu cores": "1",
        "apicid": "0",
        "initial apicid": "0",
        "fpu": "yes",
        "fpu_exception": "yes",
        "cpuid level": "22",
        "wp": "yes",
        "flags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge ...",
        "bugs": "cpu_meltdown spectre_v1 spectre_v2 spec_store_bypass ...",
        "bogomips": "4800.00",
        "clflush size": "64",
        "cache_alignment": "64",
        "address sizes": "45 bits physical, 48 bits virtual",
        "power management": ""
      },
      ...
    ]
"""
from typing import List, Dict
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`/proc/cpuinfo` file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux']
    tags = ['file']
    hidden = True


__version__ = info.version


def _process(proc_data: List[Dict]) -> List[Dict]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    for entry in proc_data:
        for key in entry:
            if entry[key] == '':
                entry[key] = None

            try:
                entry[key] = int(entry[key])
            except Exception:
                pass

            try:
                if isinstance(entry[key], str) and (entry[key] == 'yes' or entry[key] == 'no'):
                    entry[key] = jc.utils.convert_to_bool(entry[key])
            except Exception:
                pass

            try:
                if isinstance(entry[key], str) and '.' in entry[key]:
                    entry[key] = float(entry[key])
            except Exception:
                pass

        if 'address sizes' in entry:
            phy = int(entry['address sizes'].split()[0])
            virt = int(entry['address sizes'].split()[3])
            entry['address_size_physical'] = phy
            entry['address_size_virtual'] = virt

        if 'cache size' in entry:
            cache_size_int, unit = entry['cache size'].split()
            entry['cache_size_num'] = int(cache_size_int)
            entry['cache_size_unit'] = unit

        if 'flags' in entry:
            entry['flags'] = entry['flags'].split()

        if 'bugs' in entry:
            entry['bugs'] = entry['bugs'].split()

    return proc_data


def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[Dict]:
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
    output_line: Dict = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):

            if line.startswith('processor'):
                if output_line:
                    raw_output.append(output_line)
                output_line = {}

            key, val = line.split(':', maxsplit=1)
            output_line[key.strip()] = val.strip()

        if output_line:
            raw_output.append(output_line)

    return raw_output if raw else _process(raw_output)
