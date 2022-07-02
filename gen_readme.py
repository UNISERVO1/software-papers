#!/usr/bin/env python3
# usage:
# ./gen_readme.py > README.md
#
# requires pip install pyyaml

import yaml

# TODO: make the name parsing smart enough to handle lists of full names and recognize the surname
# TODO: consider adding fields for topic tags, abtract quotes, arbitrary notes

# load paper specs
with open('papers.yml') as file_:
    papers = yaml.safe_load(file_)
    papers.sort(key=lambda p: p['year'])

# set computed fields
for paper in papers:
    author = paper['authors'].split(',')[0].split(' ')[0].lower()
    year = str(paper['year'])[2:]
    paper['ref'] = f'{author}{year}'

# build table of contents
papers_toc = ''
for paper in papers:
    papers_toc += f'1. _[{paper["title"]}](#{paper["ref"]})_. {paper["authors"]} ({paper["year"]})\n'


# build detail sections
papers_notes = ''
for n, paper in enumerate(papers, start=1):
    papers_notes += f"""
### {n}. <a name="{paper['ref']}"></a> [{paper["title"]}]({paper["link"]})
* {paper["authors"]} ({paper["year"]}).
"""
    if paper.get('related'):
        papers_notes += "* Further reading:\n"
        for related in paper['related']:
            papers_notes += f'  * _[{related["title"]}]({related["link"]})_. {related["authors"]} ({related["year"]}).\n'
            pass

# inject into readme
with open('README.md.template') as template:
    # this (and the previous markdown) could be rewritten to use some templating engine,
    # but at this size I find it simpler to format manually
    output = template.read().replace('{{ PAPERS_TOC }}', papers_toc).\
        replace('{{ PAPERS_NOTES }}', papers_notes)

print(output)
