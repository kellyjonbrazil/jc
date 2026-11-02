r"""jc - JSON Convert `YAML` file parser

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
"""
import math
import jc.utils
from jc.exceptions import LibraryNotInstalled


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.9'
    description = 'YAML file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    tags = ['standard', 'file', 'string']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Each dictionary represents a YAML document.
    """
    # No further processing
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries representing the YAML documents.
    """
    # check if yaml library is installed and fail gracefully if it is not
    try:
        from ruamel.yaml import YAML
        from ruamel.yaml.constructor import RoundTripConstructor
    except Exception:
        raise LibraryNotInstalled('The ruamel.yaml library is not installed.')

    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []

    if jc.utils.has_data(data):

        # the changes below are made on subclasses so the ruamel.yaml
        # classes stay unchanged for other code in the same process

        # disable plugins since we don't use them and in ruamel.yaml
        # versions prior to 0.17.0 the use of __file__ in the plugin code
        # is incompatible with the pyoxidizer packager
        class JcYAML(YAML):
            def official_plug_ins(self):
                return []

        # add_constructor() gives the subclass its own copy of the
        # constructor table
        class JcConstructor(RoundTripConstructor):
            pass

        str_constructor = RoundTripConstructor.yaml_constructors['tag:yaml.org,2002:str']

        # modify the timestamp constructor to output datetime objects as
        # strings since JSON does not support datetime objects
        JcConstructor.add_constructor('tag:yaml.org,2002:timestamp', str_constructor)

        # modify the value constructor to output values starting with a
        # literal "=" as a string.
        JcConstructor.add_constructor('tag:yaml.org,2002:value', str_constructor)

        # load nan and inf as None since JSON does not support them
        float_constructor = RoundTripConstructor.yaml_constructors['tag:yaml.org,2002:float']

        def finite_float_constructor(constructor, node):
            value = float_constructor(constructor, node)
            if isinstance(value, float) and not math.isfinite(value):
                return None
            return value

        JcConstructor.add_constructor('tag:yaml.org,2002:float', finite_float_constructor)

        # use the default `typ` to correctly load values that start with a literal "="
        yaml = JcYAML(typ=None)
        yaml.Constructor = JcConstructor

        for document in yaml.load_all(data):
            raw_output.append(document)

        # aliases load as shared objects that are written out in full for
        # each reference, so limit how much the output can grow from them
        jc.utils.expansion_check(raw_output, len(data))

    return raw_output if raw else _process(raw_output)
