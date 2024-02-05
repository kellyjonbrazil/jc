# Contributing to jc
We love your input! We want to make contributing to this project as easy and
transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Proposing a new parser

## We Develop with Github
We use github to host code, to track issues and feature requests, as well as
accept pull requests.

## We Use Github Flow, So All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase (we use
[Github Flow](https://guides.github.com/introduction/flow/index.html)). We
actively welcome your pull requests:

1. Open an issue to discuss the new feature, bug fix, or parser before opening
   a pull request. For new parsers, it is important to agree upon a schema
   before developing the parser.
2. Fork the repo and create your branch from `dev`, if available, otherwise
   `master`.
3. For new parsers:
   - Templates: Use the [`jc/parsers/foo.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/foo.py)
     or [`jc/parsers/foo_s.py (streaming)`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/foo_s.py)
     parsers as a template to get started.
   - Local development: You can even place a new parser python module file in
     the [parser plugin directory](https://github.com/kellyjonbrazil/jc#parser-plugins)
     to get started right away with just a standard `jc` installation.
   - Parser registry: Add the parser name to the [jc/lib.py](https://github.com/kellyjonbrazil/jc/blob/master/jc/lib.py)
     file.
4. If you've added code that should be tested, add tests. All new parsers should
   have several sample outputs and tests.
   - Templates:
     - **Recommended:** [tests/templates/_test_foo_simple.py](https://github.com/kellyjonbrazil/jc/tree/master/tests/templates/_test_foo_simple.py) as a template if you only have test with fixtures.
       Execute these steps for standard tests:
       - Save this file as `test_{parser_name}.py` since the helper methods extract parser names from the filename. Use underscores instead of dashes for the parser name.
       - Organize fixtures in `tests/fixtures` for optimal structure.
       - Format fixtures as follows (using double dashes):
           - `{parser_name}--{some_test_description}.out` for command output. (no dots in the filename except for the `.out` suffix)
           - `{parser_name}--{some_test_description}.json` for expected JSON after parsing. (no dots in the filename except for the `.json` suffix)
     - Custom: [tests/templates/_test_foo.py](https://github.com/kellyjonbrazil/jc/blob/master/tests/templates/_test_foo.py) as a template for tests.
     - Custom: [tests/templates/_test_foo_s.py](https://github.com/kellyjonbrazil/jc/tree/master/tests/templates/_test_foo_s.py) as a template for **streaming parser** tests.
   - Fixtures: Tests typically consist of an input file and an expected output
     JSON file. Add the data files to the appropriate folder under [tests/fixtures](https://github.com/kellyjonbrazil/jc/tree/master/tests/fixtures)
5. Documentation is auto-generated from docstrings, so ensure they are clear and
   accurate.
6. Ensure the test suite passes. (Note: "**America/Los_Angeles**" timezone
   should be configured on the test system)
7. Make sure your code lints.
8. Issue that pull request!

## Documentation And Completions

No need to worry about documentation and completions as those are auto generated
via the python doc strings.

## Parser Schema Guidelines
- Try to keep the schema as flat as possible - typically a list of flat
  dictionaries
- Keys should be lowercase, contain no special characters, and spaces should be
  converted to underscores
- Keys should be static, if possible. If they have to be dynamic, then they
  should not contain lists or dictionaries

This will make it easier to use tools like `jq` without requiring escaping of
special characters, encapsulating key names in `[""]`, keeps paths predictable,
and makes iterating and searching for values easier.

**Examples**

Bad:
```json
{
  "Interface 1": [
    "192.168.1.1",
    "172.16.1.1"
  ],
  "Wifi Interface 1": [
    "10.1.1.1"
  ]
}
```
Good:
```json
[
  {
    "interface": "Interface 1",
    "ip_addresses": [
      "192.168.1.1",
      "172.16.1.1"
    ]
  },
  {
    "interface": "Wifi Interface 1",
    "ip_addresses": [
      "10.1.1.1"
    ]
  }
]
```

## Development Environment
Use the following steps to set up the development environment.

### Virtual Environment
Set up a Python virtual environment for `jc` development so you won't have to
worry about library conflicts. This can be done with something like
[pyenv](https://github.com/pyenv/pyenv) and/or
[venv](https://docs.python.org/3/library/venv.html)

### Clone the repo
Once the virtual environment is set up, clone the `jc` repository inside:

```bash
git clone https://github.com/kellyjonbrazil/jc.git
```

### Install In Developer Mode
Next, use the `./install.sh` script to install `jc` and the requirements in
developer mode (code chages take effect immediately). This will install the
console-script entry point to `$HOME/.local/bin` so you may need to add this
to your path.

## Tests
It is essential to have good command output sample coverage and tests to keep
the `jc` parser quality high.

Many parsers include calculated timestamp fields using the `jc.utils.timestamp`
class. Naive timestamps created with this class should be generated on a system
configured with the "**America/Los_Angeles**" timezone on linux/macOS/unix and
"**Pacific Standard Time**" timezone on Windows for tests to pass on the Github
Actions CI tests. This timezone should be configured on your local system before
running the tests locally, as well.

You can run all tests by running the `./runtests.sh` script.

## Debug Messages

Use `--debug` or `-d` to see debug error messages (double to see more):

```shell
echo 'abc' | jc --parser-with-error -dd
```

## Any contributions you make will be under the MIT Software License
In short, when you submit code changes, your submissions are understood to be
under the same [MIT License](http://choosealicense.com/licenses/mit/) that
covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's Issues
We use GitHub issues to track public bugs. Report a bug by
[opening a new issue](https://github.com/kellyjonbrazil/jc/issues); it's that
easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you
  tried that didn't work)

## Use a Consistent Coding Style

* 4 spaces for indentation rather than tabs
* Use a Python linter that will enforce PEP 8 and other best practices
