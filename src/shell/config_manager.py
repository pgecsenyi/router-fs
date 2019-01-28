import json
import os

from domain import exceptions
from domain.config import Config, LoggingConfig, TransformationConfig, VolumeConfig

SECTION_LOGGING = 'logging'
SECTION_VOLUMES = 'volumes'


class ConfigManager:

    def __init__(self, filename: str):
        self._filename = filename

    def generate_sample_configuration(self):
        logging_config = LoggingConfig()
        logging_config.enabled = True
        logging_config.path = '../data/log.txt'

        transformation_config = TransformationConfig(
            '.*/(?P<title>[^/]+)/(?P<category>[^/]+)/content/(?P<filename>.+)\\.(?P<extension>md|odt|txt)$',
            'cyclopaedia/\\g<title> [\\g<category>]/\\g<filename>.\\g<extension>')

        volume_config = VolumeConfig('../data/source', '../data/target')
        volume_config.transformations = [transformation_config]

        config = Config()
        config.logging = logging_config
        config.volumes = [volume_config]

        return config

    def load(self):
        self._assert_file_exists()

        try:
            json_config = ''
            with open(self._filename, 'r') as config_file:
                json_config = json.load(config_file)

            return self._parse_json_config(json_config)
        except KeyError as missing_key:
            raise exceptions.InvalidConfigException(
                F'Key {missing_key} is missing.')
        except Exception as exception:
            raise exceptions.ConfigManagerException(
                F'Could not parse configuration. {exception}')

    def save(self, config):
        try:
            json_config = self._create_json_config(config)

            with open(self._filename, 'w') as config_file:
                json.dump(json_config, config_file, indent=2, sort_keys=True)
        except Exception as exception:
            raise exceptions.ConfigManagerException(
                F'Could not save configuration. {exception}')

    def _assert_file_exists(self):
        if not os.path.isfile(self._filename):
            raise exceptions.ConfigManagerException(
                F'The configuration file {self._filename} does not exist.')

    def _create_json_config(self, config):
        json_config = {}

        json_config[SECTION_LOGGING] = self._create_logging_config(
            config.logging)
        json_config[SECTION_VOLUMES] = self._create_volumes_config(
            config.volumes)

        return json_config

    def _create_logging_config(self, logging_config):
        return {
            'enabled': logging_config.enabled,
            'level': logging_config.level,
            'max_size_bytes': logging_config.max_size_bytes,
            'path': logging_config.path
        }

    def _create_volumes_config(self, volumes_config):
        json_volumes = []

        for volume_config in volumes_config:
            json_volume = self._create_volume_config(volume_config)
            json_volumes.append(json_volume)

        return json_volumes

    def _create_volume_config(self, volume_config):
        json_transformations = self._create_transformations_config(
            volume_config.transformations)

        return {
            'allow_other': volume_config.allow_other,
            'mount_point': volume_config.mount_point,
            'source_path': volume_config.source_path,
            'transformations': json_transformations
        }

    def _create_transformations_config(self, transformations_config):
        json_transformations = []

        for transformation in transformations_config:
            json_transformation = {
                'from': transformation.from_path,
                'to': transformation.to_path
            }
            json_transformations.append(json_transformation)

        return json_transformations

    def _parse_json_config(self, json_config):
        config = Config()

        config.logging = self._parse_logging_config(
            json_config[SECTION_LOGGING])
        config.volumes = self._parse_volumes_config(
            json_config[SECTION_VOLUMES])

        return config

    def _parse_logging_config(self, json_config):
        logging_config = LoggingConfig()

        logging_config.enabled = json_config['enabled']
        logging_config.level = json_config['level']
        logging_config.max_size_bytes = json_config['max_size_bytes']
        logging_config.path = json_config['path']

        return logging_config

    def _parse_volumes_config(self, json_config):
        volumes_config = []

        for json_volume in json_config:
            volume_config = self._parse_volume_config(json_volume)
            volumes_config.append(volume_config)

        return volumes_config

    def _parse_volume_config(self, json_volume):
        mount_point = json_volume['mount_point']
        source_path = json_volume['source_path']

        volume_config = VolumeConfig(source_path, mount_point)

        if 'allow_other' in json_volume:
            volume_config.allow_other = json_volume['allow_other']
        if 'transformations' in json_volume:
            volume_config.transformations = self._parse_transformations_config(
                json_volume['transformations'])

        return volume_config

    def _parse_transformations_config(self, json_transformations):
        transformations = []

        for json_transformation in json_transformations:
            transformations.append(TransformationConfig(
                json_transformation['from'],
                json_transformation['to']))

        return transformations
