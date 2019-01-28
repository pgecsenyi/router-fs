import unittest
from unittest.mock import MagicMock

from domain.config import TransformationConfig
from filesystem.transformation.directory_lister import DirectoryLister
from filesystem.transformation.transformer import Transformer


class DirectoryListerTest(unittest.TestCase):

    def test_get_directory_contents(self):
        transformer = self._prepare_transformer()

        result = transformer.get_directory_contents('cyclopaedia')

        self.assertEqual(
            ['food [fruits]', 'food [vegetables]'],
            sorted(result))

    def test_get_root_directory_contents(self):
        transformer = self._prepare_transformer()

        result = transformer.get_directory_contents('/')

        self.assertEqual(['cyclopaedia'], result)

    def test_get_source_path_existing(self):
        transformer = self._prepare_transformer()

        result = transformer.get_source_path(
            'cyclopaedia/food [vegetables]/aubergine.txt')

        self.assertEqual(
            '/home/root/doc/food/vegetables/content/aubergine.txt',
            result)

    def test_get_source_path_non_existing(self):
        transformer = self._prepare_transformer()

        result = transformer.get_source_path(
            'cyclopaedia/food [vegetables]/courgette.txt')

        self.assertEqual('', result)

    def test_get_source_path_rooted(self):
        transformer = self._prepare_transformer()

        result = transformer.get_source_path(
            '/cyclopaedia/food [vegetables]/aubergine.txt')

        self.assertEqual(
            '/home/root/doc/food/vegetables/content/aubergine.txt',
            result)

    def _prepare_transformer(self):

        files = [
            '/home/root/doc/food/vegetables/content/aubergine.txt',
            '/home/root/doc/food/fruits/content/apple.md',
            '/home/root/doc/food/fruits/content/banana.odt',
            '/home/root/doc/food/fruits/draft/cherry.md']
        directory_lister = DirectoryLister('/home/root/food')
        directory_lister.list_directory = MagicMock(return_value=files)
        transformations = [
            TransformationConfig(
                '.*/(?P<title>[^/]+)/(?P<category>[^/]+)/content/(?P<filename>.+)\\.(?P<extension>md|odt|txt)$',
                'cyclopaedia/\\g<title> [\\g<category>]/\\g<filename>.\\g<extension>')
        ]

        transformer = Transformer()
        transformer.add_to_cache(directory_lister, transformations)

        return transformer
