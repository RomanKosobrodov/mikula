from mikula.implementation.md import extract_meta


def test_extract_once():
    md = '''---
key1: value1
key2: value2
---
# Header
First paragraph goes here
'''
    expected = '''# Header
First paragraph goes here
'''
    meta, content = extract_meta(md, defaults={})
    assert meta["key1"] == "value1"
    assert meta["key2"] == "value2"
    assert content == expected


def test_extract_meta_many():
    md = '''---
key1: value1
key2: value2
---
# Header
---
horizontal line
---
---
'''
    expected_content = '''# Header
---
horizontal line
---
---
'''
    meta, content = extract_meta(md, defaults={})
    assert meta["key1"] == "value1"
    assert meta["key2"] == "value2"
    assert content == expected_content


def test_extract_none():
    md = "# Header\n Lorem ipsum quaternion"
    meta, content = extract_meta(md, defaults={})
    assert len(meta.keys()) == 0
    assert content == md


def test_extract_default_meta():
    md = "# Header\n Lorem ipsum quaternion"
    defaults = {"one": 1}
    meta, content = extract_meta(md, defaults=defaults)
    assert meta == defaults


if __name__ == "__main__":
    test_extract_once()
    test_extract_meta_many()
    test_extract_none()
    test_extract_default_meta()
