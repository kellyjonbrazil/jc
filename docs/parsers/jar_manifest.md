[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.jar_manifest"></a>

# jc.parsers.jar_manifest

jc - JSON Convert Java `MANIFEST.MF` file parser

Usage (cli):

    $ cat MANIFEST.MF | jc --jar-manifest

Usage (module):

    import jc
    result = jc.parse('jar_manifest', jar_manifest_file_output)

Schema:

    [
      {
        "key1":     string,
        "key2":     string
      }
    ]

Examples:

    $ cat MANIFEST.MF | jc --jar-manifest -p
    $ unzip -c log4j-core-2.16.0.jar META-INF/MANIFEST.MF | \\
      jc --jar-manifest -p
    $ unzip -c 'apache-log4j-2.16.0-bin/*.jar' META-INF/MANIFEST.MF | \\
      jc --jar-manifest -p

    $ cat MANIFEST.MF | jc --jar-manifest -p
    [
      {
        "Import_Package": "com.conversantmedia.util.concurrent;resoluti...",
        "Export_Package": "org.apache.logging.log4j.core;uses:=\"org.ap...",
        "Manifest_Version": "1.0",
        "Bundle_License": "https://www.apache.org/licenses/LICENSE-2.0.txt",
        "Bundle_SymbolicName": "org.apache.logging.log4j.core",
        "Built_By": "matt",
        "Bnd_LastModified": "1639373735804",
        "Implementation_Vendor_Id": "org.apache.logging.log4j",
        "Specification_Title": "Apache Log4j Core",
        "Log4jReleaseManager": "Matt Sicker",
        ...
      }
    ]

    $ unzip -c 'apache-log4j-2.16.0-bin/*.jar' META-INF/MANIFEST.MF | \\
      jc --jar-manifest -p
    [
      ...
      {
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-boot-2.16.0-so...",
        "Manifest_Version": "1.0",
        "Built_By": "matt",
        "Created_By": "Apache Maven 3.8.4",
        "Build_Jdk": "1.8.0_312"
      },
      {
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-boot-2.16.0-ja...",
        "Manifest_Version": "1.0",
        "Built_By": "matt",
        "Created_By": "Apache Maven 3.8.4",
        "Build_Jdk": "1.8.0_312"
      },
      {
        "Bundle_SymbolicName": "org.apache.logging.log4j.spring-cloud-c...",
        "Export_Package": "org.apache.logging.log4j.spring.cloud.config...",
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-cloud-config-c...",
        "Manifest_Version": "1.0",
        "Bundle_License": "https://www.apache.org/licenses/LICENSE-2.0.txt",
        ...
      }
      ...
    ]

<a id="jc.parsers.jar_manifest.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
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

Source: [`jc/parsers/jar_manifest.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/jar_manifest.py)

Version 0.01 by Matt J (https://github.com/listuser)
