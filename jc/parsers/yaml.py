"""jc - JSON CLI output utility `YAML` file parser

Usage (cli):

    $ cat foo.yaml | jc --yaml

Usage (module):

    import jc.parsers.yaml
    result = jc.parsers.yaml.parse(yaml_file_output)

Schema:

    YAML Document converted to a Dictionary
    See https://pypi.org/project/ruamel.yaml for details

    [
      {
        "key1":     string/int/float/boolean/null/array/object,
        "key2":     string/int/float/boolean/null/array/object
      }
    ]

Examples:

    $ cat istio-mtls-permissive.yaml
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

    $ cat istio-mtls-permissive.yaml | jc --yaml -p
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
import sys
import jc.utils
# check if yaml library is installed and fail gracefully if it is not
try:
    from ruamel.yaml import YAML
except Exception:
    jc.utils.error_message('The ruamel.yaml library is not installed.')
    sys.exit(1)


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.4'
    description = 'YAML file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


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
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries representing the YAML documents.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    if jc.utils.has_data(data):

        # monkey patch to disable plugins since we don't use them and in
        # ruamel.yaml versions prior to 0.17.0 the use of __file__ in the
        # plugin code is incompatible with the pyoxidizer packager
        YAML.official_plug_ins = lambda a: []

        yaml = YAML(typ='safe')

        for document in yaml.load_all(data):
            raw_output.append(document)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
