# Threat model: jc (JSON Convert)

## What this project does and where untrusted input enters

jc converts the text output of CLI tools, file formats and strings into JSON, YAML or Python dictionaries. There are about 240 standard parsers and 22 streaming parsers (`*_s.py`). It is used in two ways:

- **CLI:** `some-command | jc --parser`. Output often goes to `jq`, scripts, or config management tools such as Ansible's `community.general.jc` filter.
- **Python library:** `jc.parse('parser_name', data)`, `jc.get_parser()`, or calling `jc.parsers.<name>.parse()` directly.

**All data passed to a parser is untrusted.** In practice, input can come from attacker-influenced sources: logs, `/proc` files in containers, certificates, HTTP headers, file names in `ls`/`find` output, DNS answers in `dig`, `/etc/hosts`, CSV/INI/XML/YAML/plist files, and the like. Treat any byte sequence as possible input. That includes non-UTF-8 data, very long lines, deep nesting, and data that is valid for one parser but is passed to a different one.

## Components that matter most / least

In scope (most important first):

1. `jc/parsers/*.py`: the parsers themselves, including the streaming parsers (`*_s.py`) and the shared helpers in `jc/utils.py` and `jc/streaming.py`.
2. Parsers for structured or encoded formats, where the risk is higher: `xml` (uses xmltodict/expat), `yaml` (ruamel.yaml), `plist`, `x509_cert`, `x509_csr`, `x509_crl` and other ASN.1/DER/PEM parsers (these use a vendored copy of asn1crypto in `jc/parsers/asn1crypto/`), `jwt`, `csv`, `ini`, `toml` (vendored tomli), and any parser that uses `ast.literal_eval` (such as `ss`).
3. Regex-heavy parsers. Catastrophic backtracking (ReDoS) on crafted input is a real concern.
4. `jc/cli.py` and `jc/lib.py`: argument handling, output formatting, and the `jc.parse()` dispatch.

Out of scope:

- **Magic mode** (`jc dig example.com`, `jc --magic`): it runs the command the user typed. That is by design, so it is not command injection unless an attacker can control the command line.
- **Local plugin parsers** loaded from `<user_data_dir>/jc/jcparsers/`. That directory belongs to the user and is trusted, just like their `PYTHONPATH`.
- Build, docs, and release tooling: `docgen.sh`, `mangen.py`, `readmegen.py`, `llmsgen.py`, `build-*.sh`, `pypi-upload.sh`, `snap/`, `templates/`, and the `tests/` fixtures.
- Vulnerabilities in third-party dependencies (ruamel.yaml, xmltodict, Pygments) that jc's usage does not trigger. A jc call pattern that makes one of them unsafe *is* in scope.

## How to exercise it

- Library: `python3 -c "import jc; print(jc.parse('dig', open('f').read()))"`
- Streaming: `list(jc.parse('ls_s', iter(lines)))`
- CLI: `cat input | jc --dig -p`. Use `-r` for raw output.
- Every parser has sample inputs under `tests/fixtures/<platform>/` and tests in `tests/test_<parser>.py`.
- Run the whole suite with `TZ=America/Los_Angeles python3 -m unittest discover -s tests`. Some tests depend on that timezone.
- Each parser's `info` object lists its compatible platforms and tags (`file`, `string`, `command`, `slurpable`).

## How I rate severity

jc is a parsing library with no network service and no privileges. Most of its impact reaches the scripts and pipelines that consume its output.

- **Critical:** arbitrary code execution, or reading or writing files, caused by parsing untrusted data through `jc.parse()` or the CLI. Examples: unsafe deserialization, `eval`, or a YAML or XML feature that triggers code or file access.
- **High:**
  - A small input (well under 1 MB) causes a hang for minutes, or memory blow-up out of proportion to the input. Examples: ReDoS, an infinite loop, or XML/YAML entity or alias expansion.
  - Crafted input makes a parser emit structurally misleading JSON that a reasonable consumer would trust. Examples: one record's data injecting extra keys or records, or a value moving into a security-relevant field (user, permission, IP address, certificate fields).
- **Medium:**
  - Slowdowns that scale super-linearly but need large inputs.
  - Incorrect output that is plausibly security-relevant but needs an unusual consumer to matter.
  - A streaming parser that swallows or misreports errors when `ignore_exceptions` is off.
- **Low:**
  - Unhandled exceptions or tracebacks on malformed input. jc is expected to raise `ParseError` or handle the input gracefully, so a crash is a bug, but it is not a security issue on its own.
  - Cosmetic parsing errors.

Do not report these unless they lead to something above:

- Wrong output for genuinely ambiguous input formats.
- Output differences between platforms or versions of the tool that produced the input.
- Output that is large because the input describes a large table. Table parsers (`csv`, `asciitable`, and the parsers built on the simple and sparse table helpers in `jc/parsers/universal.py`) emit every header column as a key in every record, with `null` for missing cells. Output that grows with rows × columns, or long header names repeated in each record, is expected. Only growth beyond what the input describes counts, such as shared references or entity and alias expansion.
- Large pretty-printed output (`-p`) from deeply nested input. The indentation grows with the nesting depth; the data itself is not duplicated.
- Limitations documented in a parser's docstring, for example `mount` points containing ` on `, or file names with newlines in `ls` output without `-b`.

## Parsing rules jc follows

These describe intended behavior. A parser that breaks one of them is in scope.

- Lines end at LF or CRLF. A lone CR also ends a line for `csv`, `hosts`, `jar_manifest`, `m3u`, `ics` files that use only CR, and `--slurp`. Other line-break characters (U+2028, U+2029, U+0085, VT, FF) are part of the value they appear in.
- Where the tool separates fields with spaces or tabs, other Unicode whitespace (such as NBSP or U+3000) is part of the value.
- `yaml`, `plist` and `xml` raise `ParseError` when the output would be larger than 1000 × the input size + 50 MB. Expansion below that limit is not High severity.
- CLI JSON output escapes U+0000-U+001F, DEL, the C1 controls U+0080-U+009F and lone surrogates. Other printable Unicode is written as is.
- Warning and error messages show control characters as `\xNN` escapes and shorten very long lines.

## How I'd like reports and patches

- Include the parser name, a minimal input that reproduces the issue, and the exact `jc.parse()` call or CLI command.
- Patches should be small and match the existing parser style: keep the schema stable and don't add new dependencies. Each patch should come with a fixture and a test in `tests/test_<parser>.py`.
- Parsers support Python 3.6+ syntax, so avoid newer language features in patches.

## Anything to leave alone

- Don't report that magic mode runs commands, or that local plugin parsers can run arbitrary code.
- Don't report that `--debug` or `-dd` prints tracebacks or local variables.
- JSON output escapes control characters, so ANSI or terminal escape sequences in input are not an issue unless they appear unescaped in `-C` colored output or in YAML output.

