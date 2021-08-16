import mikula.implementation.render_default as default
import mikula.implementation.render_one_page as one_page


RENDERERS = {"default": default,
             "one-page": one_page}


def render(album, error_page, pages, output_directory, theme, config):
    renderer = config.get("renderer", "default")
    module = RENDERERS.get(renderer, "default")
    page_list = module.render(album, error_page, pages, output_directory, theme, config)
    return page_list
