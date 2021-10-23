from mikula.implementation.blog import find_markdown_images


md = """
![Image of Yaktocat](https://octodex.github.com/images/yaktocat.png)
This is text. Some more text follows
![Tanuki](/home/user/Pictures/tanuki.png)
An optional part with text might also follow
![More Tanukis](/home/user/Pictures/tanuki.png "racoon dog")  
    """


def test_markdown_image_regex():
    r = find_markdown_images(md)
    assert len(r) == 3


if __name__ == "__main__":
    test_markdown_image_regex()
