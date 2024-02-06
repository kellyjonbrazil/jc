[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.pkg_index_deb"></a>

# jc.parsers.pkg\_index\_deb

jc - JSON Convert Debian Package Index file parser

Usage (cli):

    $ cat Packages | jc --pkg-index-deb

Usage (module):

    import jc
    result = jc.parse('pkg_index_deb', pkg_index_deb_output)

Schema:

    [
      {
        "package":                  string,
        "version":                  string,
        "architecture":             string,
        "section":                  string,
        "priority":                 string,
        "installed_size":           integer,
        "maintainer":               string,
        "description":              string,
        "homepage":                 string,
        "depends":                  string,
        "conflicts":                string,
        "replaces":                 string,
        "vcs_git":                  string,
        "sha256":                   string,
        "size":                     integer,
        "vcs_git":                  string,
        "filename":                 string
      }
    ]

Examples:

    $ cat Packages | jc --pkg-index-deb
    [
      {
        "package": "aspnetcore-runtime-2.1",
        "version": "2.1.22-1",
        "architecture": "amd64",
        "section": "devel",
        "priority": "standard",
        "installed_size": 71081,
        "maintainer": "Microsoft <nugetaspnet@microsoft.com>",
        "description": "Microsoft ASP.NET Core 2.1.22 Shared Framework",
        "homepage": "https://www.asp.net/",
        "depends": "libc6 (>= 2.14), dotnet-runtime-2.1 (>= 2.1.22)",
        "sha256": "48d4e78a7ceff34105411172f4c3e91a0359b3929d84d26a493...",
        "size": 21937036,
        "filename": "pool/main/a/aspnetcore-runtime-2.1/aspnetcore-run..."
      },
      {
        "package": "azure-functions-core-tools-4",
        "version": "4.0.4590-1",
        "architecture": "amd64",
        "section": "devel",
        "priority": "optional",
        "maintainer": "Ahmed ElSayed <ahmels@microsoft.com>",
        "description": "Azure Function Core Tools v4",
        "homepage": "https://docs.microsoft.com/en-us/azure/azure-func...",
        "conflicts": "azure-functions-core-tools-2, azure-functions-co...",
        "replaces": "azure-functions-core-tools-2, azure-functions-cor...",
        "vcs_git": "https://github.com/Azure/azure-functions-core-tool...",
        "sha256": "a2a4f99d6d98ba0a46832570285552f2a93bab06cebbda2afc7...",
        "size": 124417844,
        "filename": "pool/main/a/azure-functions-core-tools-4/azure-fu..."
      }
    ]

    $ cat Packages | jc --pkg-index-deb -r
    [
      {
        "package": "aspnetcore-runtime-2.1",
        "version": "2.1.22-1",
        "architecture": "amd64",
        "section": "devel",
        "priority": "standard",
        "installed_size": "71081",
        "maintainer": "Microsoft <nugetaspnet@microsoft.com>",
        "description": "Microsoft ASP.NET Core 2.1.22 Shared Framework",
        "homepage": "https://www.asp.net/",
        "depends": "libc6 (>= 2.14), dotnet-runtime-2.1 (>= 2.1.22)",
        "sha256": "48d4e78a7ceff34105411172f4c3e91a0359b3929d84d26a493...",
        "size": "21937036",
        "filename": "pool/main/a/aspnetcore-runtime-2.1/aspnetcore-run..."
      },
      {
        "package": "azure-functions-core-tools-4",
        "version": "4.0.4590-1",
        "architecture": "amd64",
        "section": "devel",
        "priority": "optional",
        "maintainer": "Ahmed ElSayed <ahmels@microsoft.com>",
        "description": "Azure Function Core Tools v4",
        "homepage": "https://docs.microsoft.com/en-us/azure/azure-func...",
        "conflicts": "azure-functions-core-tools-2, azure-functions-co...",
        "replaces": "azure-functions-core-tools-2, azure-functions-cor...",
        "vcs_git": "https://github.com/Azure/azure-functions-core-tool...",
        "sha256": "a2a4f99d6d98ba0a46832570285552f2a93bab06cebbda2afc7...",
        "size": "124417844",
        "filename": "pool/main/a/azure-functions-core-tools-4/azure-fu..."
      }
    ]

<a id="jc.parsers.pkg_index_deb.parse"></a>

### parse

```python
def parse(data: str,
          raw: bool = False,
          quiet: bool = False) -> List[JSONDictType]
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

Source: [`jc/parsers/pkg_index_deb.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/pkg_index_deb.py)

Version 1.1 by Kelly Brazil (kellyjonbrazil@gmail.com)
