import jc.parsers.csv
import jc.parsers.csv_ih
import jc.parsers.tsv
import jc.parsers.tsv_ih
import json

files = [
    ('tests/fixtures/generic/tsv_ih-dpkg-query.tsv', jc.parsers.tsv_ih),
    ('tests/fixtures/generic/tsv_ih-simple-double-quote.tsv', jc.parsers.tsv_ih),
    ('tests/fixtures/generic/tsv-dpkg-query.tsv', jc.parsers.tsv),
    ('tests/fixtures/generic/csv_ih-jagged.csv', jc.parsers.csv_ih),
]

for fname, parser in files:
    with open(fname, 'r', encoding='utf-8') as fin:
        with open(fname.split('.')[0] + '.json', 'w', encoding='utf-8') as fout:
            out = parser.parse(fin.read())
            json.dump(out, fout,  separators=(',', ':'))
