#!/usr/bin/env python3

"""
Convert parser doc string to markdown
"""
import sys
import importlib
from inspect import isfunction, signature, cleandoc
import yapf  # type: ignore

ignore_lib_functions = [
    'cast',
    'wraps',
    'lru_cache',
    'namedtuple'
]

mod_path = sys.argv[1]
mod_name = mod_path.split('.')[-1]
module = importlib.import_module(f'{mod_path}')

######## HEADER ########
header = f'''[Home](https://kellyjonbrazil.github.io/jc/)
<a id="{mod_path}"></a>

# {mod_path}
'''

summary = module.__doc__ or ''

functions = []
for attribute in dir(module):
    if isfunction(getattr(module, attribute)) \
        and not getattr(module, attribute).__name__.startswith('_'):

        if 'jc.parsers.' in mod_path and not 'universal' in mod_path:
            if attribute == 'parse':
                functions.append(attribute)

        else:
            if not attribute in ignore_lib_functions:
                functions.append(attribute)

######## TABLE OF CONTENTS ########
toc = f'## Table of Contents\n\n* [{mod_path}](#{mod_path})\n'
for api in functions:
    toc = f'{toc}  * [{api}](#{mod_path}.{api})\n'

######## API DOCS ########
api_docs = ''
for api in functions:
    api_function = getattr(module, api)

    this_header = f'<a id="{mod_path}.{api}"></a>\n\n### {api}\n'
    this_sig = str(signature(api_function))
    formatted_sig = yapf.yapf_api.FormatCode(f'def {api_function.__name__}{this_sig}:\n    pass' )
    formatted_sig = formatted_sig[0].split(':\n    pass')[0]
    this_name_and_sig = f'{this_header}\n```python\n{formatted_sig}\n```'

    this_doc = cleandoc(api_function.__doc__)
    api_docs = api_docs + this_name_and_sig + '\n\n' + this_doc + '\n\n'

######## FOOTER ########
footer = ''
if 'jc.parsers.' in mod_path and not 'universal' in mod_path:
    footer = '### Parser Information\n'
    comp = ', '.join(module.info.compatible)
    ver = module.info.version
    author = module.info.author
    author_email = module.info.author_email
    slurpable = 'slurpable' in module.info.tags
    footer = footer + f'Compatibility:  {comp}\n\n'
    footer = footer + f'Source: [`jc/parsers/{mod_name}.py`](https://github.com/kellyjonbrazil/jc/blob/master/jc/parsers/{mod_name}.py)\n\n'
    if slurpable:
        footer = footer + 'This parser can be used with the `--slurp` command-line option.\n\n'
    footer = footer + f'Version {ver} by {author} ({author_email})'

final_doc = ''
if 'jc.parsers.' in mod_path and not 'universal' in mod_path:
    final_doc = header + '\n' + summary + '\n' + api_docs + footer
elif mod_path == 'jc':
    final_doc = header + '\n' + summary
else:
    final_doc = header + '\n' + toc + '\n' + summary + '\n\n' + api_docs

print(final_doc)
