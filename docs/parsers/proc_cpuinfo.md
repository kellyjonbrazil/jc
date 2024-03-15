[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.proc_cpuinfo"></a>

# jc.parsers.proc_cpuinfo

jc - JSON Convert `/proc/cpuinfo` file parser

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

<a id="jc.parsers.proc_cpuinfo.parse"></a>

### parse

```python
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[Dict]
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

### Parser Information
Compatibility:  linux

Source: [`jc/parsers/proc_cpuinfo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/proc_cpuinfo.py)

Version 1.0 by Kelly Brazil (kellyjonbrazil@gmail.com)
