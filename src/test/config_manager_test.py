import os
import unittest

from domain import exceptions
from domain.config import Config, LoggingConfig, VolumeConfig, TransformationConfig
from shell.config_manager import ConfigManager


class ConfigManagerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_config_filename = '../data/test_config.json'

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.test_config_filename)

    def test_configmanager_load(self):
        # Arrange.
        config_manager = ConfigManager(self.test_config_filename)

        logging_config = LoggingConfig()
        logging_config.enabled = True
        logging_config.level = 'critical'
        logging_config.max_size_bytes = 10000
        logging_config.path = 'path/to/logfile.txt'

        transformation_config_1 = TransformationConfig('from1', 'to1')
        transformation_config_2 = TransformationConfig('from2', 'to2')
        transformations_config = [
            transformation_config_1,
            transformation_config_2]

        volume_config = VolumeConfig('/mount/disk', '/home/root/transformed')
        volume_config.allow_other = True
        volume_config.transformations = transformations_config

        test_config = Config()
        test_config.logging = logging_config
        test_config.volumes = [volume_config]

        # Act.
        config_manager.save(test_config)
        loaded_config = config_manager.load()

        # Assert.
        self.assertTrue(loaded_config.logging.enabled)
        self.assertEqual('critical', loaded_config.logging.level)
        self.assertEqual(10000, loaded_config.logging.max_size_bytes)
        self.assertEqual('path/to/logfile.txt', loaded_config.logging.path)
        self.assertEqual(1, len(loaded_config.volumes))
        self.assertTrue(loaded_config.volumes[0].allow_other)
        self.assertEqual(
            '/home/root/transformed',
            loaded_config.volumes[0].mount_point)
        self.assertEqual('/mount/disk', loaded_config.volumes[0].source_path)
        self.assertEqual(2, len(loaded_config.volumes[0].transformations))
        self.assertEqual(
            'from1', loaded_config.volumes[0].transformations[0].from_path)
        self.assertEqual(
            'to1', loaded_config.volumes[0].transformations[0].to_path)
        self.assertEqual(
            'from2', loaded_config.volumes[0].transformations[1].from_path)
        self.assertEqual(
            'to2', loaded_config.volumes[0].transformations[1].to_path)

    def test_configmanager_nonexistent(self):
        config_manager = ConfigManager('nonexistent-file')

        with self.assertRaises(exceptions.ConfigManagerException):
            config_manager.load()
