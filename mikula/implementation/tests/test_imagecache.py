from mikula.implementation.image_cache import ImageCache
import tempfile
import os
import time
import shutil


def clean_up():
    db_dir = os.path.join(os.getcwd(), ".mikula")
    shutil.rmtree(db_dir)


def make_temp_files():
    image_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    scaled_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    thumbnail_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    return image_file.name, scaled_file.name, thumbnail_file.name


def test_imagecache_update():
    image_fn, scaled_fn, thumbnail_fn = make_temp_files()
    ic = ImageCache(os.getcwd())
    ic.update(image_fn, scaled_fn, thumbnail_fn)
    assert image_fn in ic.cache.keys()
    clean_up()


def test_imagecache_require_update_false():
    image_fn, scaled_fn, thumbnail_fn = make_temp_files()
    ic = ImageCache(os.getcwd())
    ic.update(image_fn, scaled_fn, thumbnail_fn)
    assert not ic.require_update(image_fn)
    assert ic.get_filenames() == (scaled_fn, thumbnail_fn)
    clean_up()


def test_imagecache_require_update_missing():
    image_fn, scaled_fn, thumbnail_fn = make_temp_files()
    ic = ImageCache(os.getcwd())
    ic.update(image_fn, scaled_fn, thumbnail_fn)
    assert ic.require_update("/this/file/is/missing")
    assert ic.get_filenames() is None
    clean_up()


def test_imagecache_require_update_scaled_removed():
    image_fn, scaled_fn, thumbnail_fn = make_temp_files()
    ic = ImageCache(os.getcwd())
    ic.update(image_fn, scaled_fn, thumbnail_fn)
    os.remove(scaled_fn)
    assert ic.require_update("/this/file/is/missing")
    assert ic.get_filenames() is None
    clean_up()


def test_imagecache_require_update_thumbnail_removed():
    image_fn, scaled_fn, thumbnail_fn = make_temp_files()
    ic = ImageCache(os.getcwd())
    ic.update(image_fn, scaled_fn, thumbnail_fn)
    os.remove(thumbnail_fn)
    assert ic.require_update("/this/file/is/missing")
    assert ic.get_filenames() is None
    clean_up()


def test_imagecache_require_update_image_modified():
    image_fn, scaled_fn, thumbnail_fn = make_temp_files()
    ic = ImageCache(os.getcwd())
    ic.update(image_fn, scaled_fn, thumbnail_fn)
    time.sleep(0.1)
    with open(image_fn, "w") as f:
        pass
    assert ic.require_update(image_fn)
    assert ic.get_filenames() is None
    clean_up()


def test_imagecache_require_update_scaled_modified():
    image_fn, scaled_fn, thumbnail_fn = make_temp_files()
    ic = ImageCache(os.getcwd())
    ic.update(image_fn, scaled_fn, thumbnail_fn)
    time.sleep(0.1)
    with open(scaled_fn, "w") as f:
        pass
    assert ic.require_update(image_fn)
    assert ic.get_filenames() is None
    clean_up()


def test_imagecache_require_update_thumbnail_modified():
    image_fn, scaled_fn, thumbnail_fn = make_temp_files()
    ic = ImageCache(os.getcwd())
    ic.update(image_fn, scaled_fn, thumbnail_fn)
    time.sleep(0.1)
    with open(thumbnail_fn, "w") as f:
        pass
    assert ic.require_update(image_fn)
    assert ic.get_filenames() is None
    clean_up()


def test_imagecache_config():
    ic = ImageCache(os.getcwd())
    config = {"one": 1, "two": 2, "three": 3}
    assert ic.config_changed(config)

    ic.update_config(config)
    assert not ic.config_changed(config)

    config["one"] = "uno"
    assert ic.config_changed(config)

    clean_up()


if __name__ == "__main__":
    test_imagecache_update()
    test_imagecache_require_update_false()
    test_imagecache_require_update_missing()
    test_imagecache_require_update_scaled_removed()
    test_imagecache_require_update_thumbnail_removed()
    test_imagecache_require_update_image_modified()
    test_imagecache_require_update_scaled_modified()
    test_imagecache_require_update_thumbnail_modified()
    test_imagecache_config()
