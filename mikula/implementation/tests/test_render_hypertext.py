from mikula.implementation.hypertext import render_hypertext
import tempfile
import os

CONTENT = """---
title: test content
author: mikula
version: 0.0.1
---
<h1>Header</h1>
<p>Lorem ipsum</p>
<a href="#">Link</a>
<h2>{{title}}</h2>
<p>{{author}} {{version}}</p> 
"""

RENDERED = """<h1>Header</h1>
<p>Lorem ipsum</p>
<a href="#">Link</a>
<h2>test content</h2>
<p>mikula 0.0.1</p>"""

META = {'title': 'test content',
        'author': 'mikula',
        'version': '0.0.1'}


def test_render_hypertext():
    user_file = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
    with open(user_file.name, "w") as f:
        f.write(CONTENT)

    meta, html = render_hypertext(user_file.name)
    os.remove(user_file.name)

    assert html.strip() == RENDERED.strip()
    assert meta == META


if __name__ == "__main__":
    test_render_hypertext()
