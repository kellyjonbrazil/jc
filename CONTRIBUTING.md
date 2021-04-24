# Contributing to jc
We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Proposing a new parser

## We Develop with Github
We use github to host code, to track issues and feature requests, as well as accept pull requests.

## We Use Github Flow, So All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase (we use [Github Flow](https://guides.github.com/introduction/flow/index.html)). We actively welcome your pull requests:

1. Open an issue to discuss the new feature, bug fix, or parser before opening a pull request. For new parsers, it is important to agree upon a schema before developing the parser.
2. Fork the repo and create your branch from `dev`, if available, otherwise `master`.
3. If you've added code that should be tested, add tests. All new parsers should have several sample outputs and tests.
4. Documentation is auto-generated from docstrings, so ensure they are clear and accurate.
5. Ensure the test suite passes. (Note: "America/Los_Angeles" timezone should be configured on the test system)
6. Make sure your code lints.
7. Issue that pull request!

## Parser Schema Guidelines
- Try to keep the schema as flat as possible - typically a list of flat dictionaries
- Keys should be lowercase, contain no special characters, and spaces should be converted to underscores
- Keys should be static, if possible. If they have to be dynamic, then they should not contain lists or dictionaries

This will make it easier to use tools like `jq` without requiring escaping of special characters, encapsulating key names in [""], keeps paths predictable, and makes iterating and searching for values easier.

**Examples**

Bad:
```
{
  "Interface 1": [
    192.168.1.1,
    172.16.1.1
  ],
  "Wifi Interface 1": [
    10.1.1.1
  ]
}
```
Good:
```
[
  {
    "interface": "Interface 1",
    "ip_addresses": [
      192.168.1.1,
      172.16.1.1
    ]
  },
  {
    "interface": "Wifi Interface 1",
    "ip_addresses": [
      10.1.1.1
    ]
  }
]
```

## Tests
It is essential to have good command output sample coverage and tests to keep the `jc` parser quality high.

Many parsers include calculated timestamp fields using the `jc.utils.timestamp` class. Naive timestamps created with this class should be generated on a system configured with the "**America/Los_Angeles**" timezone on linux/macOS/unix and "**Pacific Standard Time**" timezone on Windows for tests to pass on the Github Actions CI tests. This timezone should be configured on your local system before running the tests locally, as well.

## Any contributions you make will be under the MIT Software License
In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's Issues
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/kellyjonbrazil/jc/issues); it's that easy!

## Write bug reports with detail, background, and sample code
**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Use a Consistent Coding Style
* 4 spaces for indentation rather than tabs
* Use a Python linter that will enforce PEP 8 and other best practices
