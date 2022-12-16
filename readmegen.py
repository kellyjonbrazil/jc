#!/usr/bin/env python3
# Generate README.md from jc metadata using jinja2 templates
import jc.cli
import jc.lib
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('readme_template')
# output = template.render(jc=jc.cli.about_jc())
output = template.render(parsers=jc.lib.all_parser_info(),
                         info=jc.cli.JcCli.about_jc())

with open('README.md', 'w') as f:
    f.write(output)
