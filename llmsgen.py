#!/usr/bin/env python3
# Generate llms-full.txt (an LLM-readable index of every jc parser) from jc
# metadata using jinja2 templates
import sys
import jc.lib
from jinja2 import Environment, FileSystemLoader

DOCS_URL = 'https://raw.githubusercontent.com/kellyjonbrazil/jc/master/docs/parsers'
ALL_PLATFORMS = {'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'}


def build_entry(parser):
    """Turn one parser's metadata into the fields the template renders."""
    notes = []

    magic = parser.get('magic_commands')
    if magic:
        notes.append('magic: ' + ', '.join('`{}`'.format(m) for m in magic))

    platforms = parser.get('compatible', [])
    if platforms and set(platforms) != ALL_PLATFORMS:
        notes.append('platforms: ' + ', '.join(platforms))

    if 'slurpable' in parser.get('tags', []):
        notes.append('supports `--slurp`')

    return {
        'argument': parser['argument'],
        'url': '{}/{}.md'.format(DOCS_URL, parser['name']),
        'description': parser['description'],
        'notes': notes
    }


def main(output_path):
    parsers = jc.lib.all_parser_info()
    hidden = [p for p in jc.lib.all_parser_info(show_hidden=True) if p.get('hidden')]

    env = Environment(loader=FileSystemLoader('templates'),
                      trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('llms_full_template')
    output = template.render(
        version=jc.lib.__version__,
        docs_url=DOCS_URL,
        parsers=[build_entry(p) for p in parsers if not p.get('streaming')],
        streaming=[build_entry(p) for p in parsers if p.get('streaming')],
        hidden_count=len(hidden))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'llms-full.txt')
