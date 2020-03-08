import os
import shutil


MIKULA_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def customize(theme, prototype, destination):
    prototype_path = prototype
    if not os.path.isdir(prototype_path):
        prototype_path = os.path.join(MIKULA_DIRECTORY, "themes", prototype_path)
    if not os.path.isdir(prototype_path):
        print(f'Unable to find theme "{prototype_path}"')
        return

    if not os.path.isdir(destination):
        try:
            os.mkdir(destination)
        except:
            print(f'Unable to create destination directory "{destination}"')
            return

    destination_path = os.path.join(destination, theme)

    shutil.copytree(prototype_path, destination_path, dirs_exist_ok=True)
    print(f'Custom theme has been created in "{destination_path}"')
    print("Start tweaking it by modifying styles and Jinja2 templates.")
    print(f'Run `mikula build --theme {theme}` to generate gallery using your custom theme.')

