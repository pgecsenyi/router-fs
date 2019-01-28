import unittest
from unittest.mock import patch

from filesystem.transformation.directory_lister import DirectoryLister


class DirectoryListerTest(unittest.TestCase):

    @patch('os.walk')
    def test_list_directory(self, mock_walk):
        dirpath = '/home/root/doc/fruits'
        expected_files = [dirpath + '/apple.txt', dirpath + '/banana.txt']
        mock_walk.return_value = [(dirpath, [], ['apple.txt', 'banana.txt'])]

        directory_lister = DirectoryLister(dirpath)
        result = [i for i in directory_lister.list_directory()]

        mock_walk.assert_called_once_with(dirpath)
        self.assertEqual(sorted(expected_files), sorted(result))
