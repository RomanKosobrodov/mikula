from sqlitedict import SqliteDict
import os


def query(cache, filename):
    if filename not in cache.keys():
        return None
    timestamp, scaled, scaled_time, thumbnail, thumbnail_time = cache[filename]
    if get_creation_time(filename) == timestamp and \
            get_creation_time(scaled) == scaled_time and \
            get_creation_time(thumbnail) == thumbnail_time:
        return scaled, thumbnail
    return None


def get_creation_time(filename):
    if filename is not None and os.path.exists(filename):
        return os.path.getmtime(filename)
    return None


class ImageCache:
    def __init__(self, directory):
        db_dirname = os.path.join(directory, ".mikula")
        if not os.path.isdir(db_dirname):
            os.mkdir(db_dirname)
        db_filename = os.path.join(db_dirname, "images.cache")
        self.cache = SqliteDict(db_filename)
        self.recent_lookup_ = None

    def to_dictionary(self):
        return dict(self.cache.items())

    def reset(self):
        self.cache.clear()
        self.recent_lookup_ = None

    def config_changed(self, config):
        if "config" not in self.cache.keys():
            return True
        stored = self.cache["config"]
        return stored != config

    def update_config(self, config):
        self.cache["config"] = config
        self.cache.commit()

    def require_update(self, filename):
        found = query(self.cache, filename)
        if found is None:
            self.recent_lookup_ = None
            return True
        else:
            self.recent_lookup_ = found
            return False

    def get_filenames(self):
        return self.recent_lookup_

    def update(self, filename, scaled, thumbnail):
        timestamp = get_creation_time(filename)
        scaled_time = get_creation_time(scaled)
        thumbnail_time = get_creation_time(thumbnail)
        self.cache[filename] = (timestamp,
                                scaled,
                                scaled_time,
                                thumbnail,
                                thumbnail_time)
        self.cache.commit()
