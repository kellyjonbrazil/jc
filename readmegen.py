#!/usr/bin/env python3
# Genereate README.md from jc metadata using jinja2 templates
import jc.cli
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('readme_template')

# get parser info from jc.cli.about_jc()
# plug it into the man page jinja2 template
output = template.render(jc=jc.cli.about_jc())

# save to man/jc.1
with open('README.md', 'w') as f:
    f.write(output)
