[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.yaml"></a>

# jc.parsers.yaml

jc - JSON Convert `YAML` file parser

> Note: `datetime` objects will be converted to strings.

Usage (cli):

    $ cat foo.yaml | jc --yaml

Usage (module):

    import jc
    result = jc.parse('yaml', yaml_file_output)

Schema:

YAML Document converted to a Dictionary.
See https://pypi.org/project/ruamel.yaml for details.

    [
      {
        "key1":     string/int/float/boolean/null/array/object,
        "key2":     string/int/float/boolean/null/array/object
      }
    ]

Examples:

    $ cat file.yaml
    apiVersion: "authentication.istio.io/v1alpha1"
    kind: "Policy"
    metadata:
      name: "default"
      namespace: "default"
    spec:
      peers:
      - mtls: {}
    ---
    apiVersion: "networking.istio.io/v1alpha3"
    kind: "DestinationRule"
    metadata:
      name: "default"
      namespace: "default"
    spec:
      host: "*.default.svc.cluster.local"
      trafficPolicy:
        tls:
          mode: ISTIO_MUTUAL

    $ cat file.yaml | jc --yaml -p
    [
      {
        "apiVersion": "authentication.istio.io/v1alpha1",
        "kind": "Policy",
        "metadata": {
          "name": "default",
          "namespace": "default"
        },
        "spec": {
          "peers": [
            {
              "mtls": {}
            }
          ]
        }
      },
      {
        "apiVersion": "networking.istio.io/v1alpha3",
        "kind": "DestinationRule",
        "metadata": {
          "name": "default",
          "namespace": "default"
        },
        "spec": {
          "host": "*.default.svc.cluster.local",
          "trafficPolicy": {
            "tls": {
              "mode": "ISTIO_MUTUAL"
            }
          }
        }
      }
    ]

<a id="jc.parsers.yaml.parse"></a>

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

    List of Dictionaries representing the YAML documents.

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Source: [`jc/parsers/yaml.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/yaml.py)

Version 1.8 by Kelly Brazil (kellyjonbrazil@gmail.com)
