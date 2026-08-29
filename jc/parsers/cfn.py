r"""
jc - JSON Convert `CloudFormation` file parser

> Note: `datetime` objects will be converted to strings.

Usage (cli):

    $ cat template.yaml | jc --cfn

Usage (module):

    import jc
    result = jc.parse('cfn', yaml_file_output)

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

    $ cat template.yaml
    AWSTemplateFormatVersion: "2010-09-09"
    Parameters:
      EnvType:
        Type: "String"
        Default: "test"
    Conditions:
      CreateProdResources: !Equals [ !Ref EnvType, prod ]
    Resources:
      MyInstance:
        Type: "AWS::EC2::Instance"
        Properties:
          ImageId: "ami-1234567890abcdefg"
          InstanceType: "t2.micro"


    $ cat template.yaml | jc --cfn -p
    [
      {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Parameters": {
          "EnvType": {
            "Type": "String",
            "Default": "test"
          }
        },
        "Conditions": {
          "CreateProdResources": [
            "EnvType",
            "prod"
          ]
        },
        "Resources": {
          "MyInstance": {
            "Type": "AWS::EC2::Instance",
            "Properties": {
              "ImageId": "ami-1234567890abcdefg",
              "InstanceType": "t2.micro"
            }
          }
        }
      }
    ]
"""
from dataclasses import dataclass
from enum import Enum
from typing import List
import jc.utils
from jc.exceptions import LibraryNotInstalled


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.7'
    description = 'YAML file parser'
    author = 'Ron Green'
    author_email = '11993626+georgettica@users.noreply.github.com'
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

class Option(Enum):
    scalar = 1
    sequence = 2
    mapping = 3


@dataclass
class CustomTag:
    name: str
    options: List[Option]


custom_tags = [
    CustomTag(name='!And', options=[Option.sequence]),
    CustomTag(name='!Base64', options=[Option.scalar]),
    CustomTag(name='!Cidr', options=[Option.scalar]),
    CustomTag(name='!Condition', options=[Option.scalar]),
    CustomTag(name='!Equals', options=[Option.scalar, Option.sequence]),
    CustomTag(name='!FindInMap', options=[Option.sequence]),
    CustomTag(name='!GetAZs', options=[Option.scalar]),
    CustomTag(name='!GetAtt', options=[Option.scalar]),  # , Option.sequence]),
    CustomTag(name='!If', options=[Option.sequence]),
    CustomTag(name='!ImportValue', options=[Option.scalar]),
    CustomTag(name='!Join', options=[Option.sequence]),
    CustomTag(name='!Not', options=[Option.sequence]),
    CustomTag(name='!Or', options=[Option.sequence]),
    CustomTag(name='!Ref', options=[Option.scalar]),
    CustomTag(name='!Select', options=[Option.sequence]),
    CustomTag(name='!Split', options=[Option.sequence]),
    CustomTag(name='!Sub', options=[Option.scalar]),
    CustomTag(name='!Transform', options=[Option.mapping]),
]


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
        from ruamel.yaml.constructor import SafeConstructor

    except Exception:
        raise LibraryNotInstalled('The ruamel.yaml library is not installed.')

    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = []

    if jc.utils.has_data(data):

        # monkey patch to disable plugins since we don't use them and in
        # ruamel.yaml versions prior to 0.17.0 the use of __file__ in the
        # plugin code is incompatible with the pyoxidizer packager
        YAML.official_plug_ins = lambda a: []

        yaml = YAML(typ='safe')
        for custom_tag in custom_tags:
          for option in custom_tag.options:
              if option == Option.mapping:
                yaml.constructor.add_constructor(custom_tag.name, lambda loader, node: loader.construct_mapping(node))
                continue
              if option == Option.sequence:
                  yaml.constructor.add_constructor(custom_tag.name, lambda loader, node: loader.construct_sequence(node))
                  continue
              if option == Option.scalar:
                  yaml.constructor.add_constructor(custom_tag.name, lambda loader, node: loader.construct_scalar(node))
                  continue
              
        # yaml.Constructor = SafeConstructor
        # modify the timestamp constructor to output datetime objects as
        # strings since JSON does not support datetime objects
        yaml.constructor.yaml_constructors['tag:yaml.org,2002:timestamp'] = \
            yaml.constructor.yaml_constructors['tag:yaml.org,2002:str']
        
        


        for document in yaml.load_all(data):
            raw_output.append(document)

    if raw:
        return raw_output
    else:
        return _process(raw_output)
