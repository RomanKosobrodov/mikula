from sqlitedict import SqliteDict
import os


class ImageCache:
    def __init__(self, directory):
        db_dirname = os.path.join(directory, ".mikula")
        if not os.path.isdir(db_dirname):
            os.mkdir(db_dirname)
        db_filename = os.path.join(db_dirname, "images.cache")
        self.cache = SqliteDict(db_filename)
        self.recent_lookup_ = None

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
        if filename not in self.cache.keys():
            self.recent_lookup_ = None
            return True

        timestamp, scaled, scaled_time, thumbnail, thumbnail_time = self.cache[filename]
        if os.path.exists(scaled) and os.path.exists(thumbnail):
            if os.path.getmtime(filename) == timestamp and \
               os.path.getmtime(scaled) == scaled_time and \
               os.path.getmtime(thumbnail) == thumbnail_time:
                self.recent_lookup_ = (scaled, thumbnail)
                return False
        self.recent_lookup_ = None
        return True

    def get_filenames(self):
        return self.recent_lookup_

    def update(self, filename, scaled, thumbnail):
        timestamp = os.path.getmtime(filename)
        scaled_time = os.path.getmtime(scaled)
        thumbnail_time = os.path.getmtime(thumbnail)
        self.cache[filename] = (timestamp,
                                scaled,
                                scaled_time,
                                thumbnail,
                                thumbnail_time)
        self.cache.commit()
