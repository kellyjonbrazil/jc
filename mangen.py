#!/usr/bin/env python3
# Genereate man page from jc metadata using jinja2 templates
from datetime import date
import os
import gzip
import shutil
import jc.cli
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('manpage_template')
output = template.render(today=date.today(),
                         jc=jc.cli.about_jc())

with open('man/jc.1', 'w') as f:
    f.write(output)
