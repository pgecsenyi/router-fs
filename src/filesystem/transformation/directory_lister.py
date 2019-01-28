import os


class DirectoryLister:

    def __init__(self, source_directory):
        self._source_directory = source_directory

    def list_directory(self):
        for dirname, _, filenames in os.walk(self._source_directory):
            for filename in filenames:
                yield os.path.join(dirname, filename)
