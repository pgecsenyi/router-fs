import os
import re


class Transformer:

    def __init__(self):
        self._cache = {}
        self._full_path_cache = {}

    def add_to_cache(self, directory_lister, transformations):
        pattern_pairs = [
            (re.compile(transformation.from_path), transformation.to_path)
            for transformation
            in transformations
        ]
        paths = directory_lister.list_directory()
        transformed_paths = self._transform_paths(paths, pattern_pairs)

        self._build_cache(transformed_paths)

    def get_directory_contents(self, path):
        if path == os.sep:
            return list(self._cache.keys())

        parts = path.split(os.sep)

        current_cache = self._cache

        for part in parts:
            if part == '':
                continue
            if part not in current_cache:
                return list(current_cache.keys())
            current_cache = current_cache[part]

        return list(current_cache.keys())

    def get_source_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        if path in self._full_path_cache:
            return self._full_path_cache[path]

        return ''

    def _transform_paths(self, paths, patterns):
        for path in paths:
            for pattern_pair in patterns:
                source_regexp = pattern_pair[0]
                target_pattern = pattern_pair[1]
                if source_regexp.match(path):
                    yield source_regexp.sub(target_pattern, path), path
                    break

    def _build_cache(self, paths):
        for path in paths:
            source = path[1]
            target = path[0]
            parts = target.split(os.sep)

            current_cache = self._cache
            current_level = 0
            deepest_level = len(parts) - 1

            for part in parts:
                if current_level < deepest_level:
                    current_cache.setdefault(part, {})
                    current_cache = current_cache[part]
                    current_level = current_level + 1
                else:
                    current_cache[part] = source
                    self._full_path_cache[target] = source
                    break
