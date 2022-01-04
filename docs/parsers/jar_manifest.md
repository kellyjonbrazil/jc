[Home](https://kellyjonbrazil.github.io/jc/)

# jc.parsers.jar_manifest
jc - JSON CLI output utility `MANIFEST.MF` file parser

Usage (cli):

    $ cat MANIFEST.MF | jc --jar-manifest

Usage (module):

    import jc.parsers.jar_manifest
    result = jc.parsers.jar_manifest.parse(jar_manifest_file_output)

Schema:

    [
      {
        "key1":     string,
        "key2":     string
      }
    ]

Examples:

    $ cat MANIFEST.MF | jc --jar-manifest -p
    $ unzip -c apache-log4j-2.16.0-bin/log4j-core-2.16.0.jar META-INF/MANIFEST.MF | jc --jar-manifest -p
    $ unzip -c 'apache-log4j-2.16.0-bin/*.jar' META-INF/MANIFEST.MF | jc --jar-manifest -p

    $ cat MANIFEST.MF | jc --jar-manifest -p

    [
      {
        "Import_Package": "com.conversantmedia.util.concurrent;resolution:=optional,com.fasterxml.jackson.annotation;version="[2.12,3)";resolution:=optional,com.fasterxml.jackson.core;version="[2.12,3)";resolution:=optional,com.fasterxml.jackson.core.type;version="[2.12,3)";resolution:=optional,com.fasterxml.jackson.cor...",
        "Export_Package": "org.apache.logging.log4j.core;uses:="org.apache.logging.log4j,org.apache.logging.log4j.core.config,org.apache.logging.log4j.core.impl,org.apache.logging.log4j.core.layout,org.apache.logging.log4j.core.time,org.apache.logging.log4j.message,org.apache.logging.log4j.spi,org.apache.logging.log4j.status...",
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

    $ unzip -c 'apache-log4j-2.16.0-bin/*.jar' META-INF/MANIFEST.MF | jc --jar-manifest -p

    [
      ...
      {
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-boot-2.16.0-sources.jar",
        "Manifest_Version": "1.0",
        "Built_By": "matt",
        "Created_By": "Apache Maven 3.8.4",
        "Build_Jdk": "1.8.0_312"
      },
      {
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-boot-2.16.0-javadoc.jar",
        "Manifest_Version": "1.0",
        "Built_By": "matt",
        "Created_By": "Apache Maven 3.8.4",
        "Build_Jdk": "1.8.0_312"
      },
      {
        "Bundle_SymbolicName": "org.apache.logging.log4j.spring-cloud-config-client.logging.log4j.core.util;version="[2.16,3)",org.springframework.boot.autoconfigure.condition,org.springframework.cloud.context.environment,org.springframework.context,org.springframework.stereotype",
        "Export_Package": "org.apache.logging.log4j.spring.cloud.config.controller;version="2.16.0"ient",
        "Archive": "apache-log4j-2.16.0-bin/log4j-spring-cloud-config-client-2.16.0.jar",
        "Manifest_Version": "1.0",
        "Bundle_License": "https://www.apache.org/licenses/LICENSE-2.0.txt",
        ...
      }
      ...
    ]


## info
```python
info()
```
Provides parser metadata (version, author, etc.)

## parse
```python
parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) output preprocessed JSON if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    List of Dictionaries. Raw or processed structured data.

## Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Version 0.01 by Matt J (https://github.com/listuser)
