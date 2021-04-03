#!/usr/bin/env python3
# Genereate man page from jc metadata using jinja2 templates
from datetime import date
import jc
import jc.cli
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('man/template')
env = Environment(loader=file_loader)
template = env.get_template('manpage_template')

# get parser info from jc.cli.about_jc()
# plug it into the man page jinja2 template
jcinfo = jc.cli.about_jc()
today = date.today()
output = template.render(today=today, jc=jcinfo)

# save to man/jc.1
with open('man/jc.1', 'w') as f:
    f.write(output)
