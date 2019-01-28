import unittest

from domain import exceptions
from domain.config import TransformationConfig, VolumeConfig
from filesystem.mirror_fs import MirrorFs
from filesystem.transformer_fs import TransformerFs
from shell.proxy_factory import ProxyFactory


class ProxyFactoryTest(unittest.TestCase):

    def test_create_proxies_mirror(self):
        volume = VolumeConfig('data', '/mnt/new_volume')
        volumes = [volume]

        proxy_factory = ProxyFactory()
        proxies = proxy_factory.create_proxies(volumes)

        self.assertEqual(1, len(proxies))
        self.assertEqual('/mnt/new_volume', proxies[0].mount_point)
        self.assertIsInstance(proxies[0].fuse_fs.__class__, type(MirrorFs))

    def test_create_proxies_mirrors(self):
        # Arrange.
        volume1 = VolumeConfig('data', '/mnt/new_volume')
        volume2 = VolumeConfig('data2', '/mnt/new_volume_2')
        volumes = [volume1, volume2]

        # Act.
        proxy_factory = ProxyFactory()
        proxies = proxy_factory.create_proxies(volumes)

        # Assert.
        self.assertEqual(2, len(proxies))
        self.assertEqual('/mnt/new_volume', proxies[0].mount_point)
        self.assertIsInstance(proxies[0].fuse_fs.__class__, type(MirrorFs))
        self.assertEqual('/mnt/new_volume_2', proxies[1].mount_point)
        self.assertIsInstance(proxies[1].fuse_fs.__class__, type(MirrorFs))

    def test_create_proxies_mirrors_same_mount_point(self):
        volume1 = VolumeConfig('data', '/mnt/new_volume')
        volume2 = VolumeConfig('data2', '/mnt/new_volume')
        volumes = [volume1, volume2]

        proxy_factory = ProxyFactory()

        try:
            proxy_factory.create_proxies(volumes)
        except exceptions.InvalidConfigException:
            return

        self.fail(
            F'Expected to throw an {type(exceptions.InvalidConfigException)}.')

    def test_create_proxies_transformer(self):
        transformation = TransformationConfig(
            'dir/(?P<title>[^/]+).csv', '\\g<title>.csv')
        volume = VolumeConfig('data', '/mnt/new_volume')
        volume.transformations = [transformation]
        volumes = [volume]

        proxy_factory = ProxyFactory()
        proxies = proxy_factory.create_proxies(volumes)

        self.assertEqual(1, len(proxies))
        self.assertEqual('/mnt/new_volume', proxies[0].mount_point)
        self.assertIsInstance(
            proxies[0].fuse_fs.__class__,
            type(TransformerFs))

    def test_create_proxies_mirror_and_transformer(self):
        # Arrange.
        volume_mirror = VolumeConfig('data1', '/mnt/new_volume')

        transformation = TransformationConfig(
            'dir/(?P<title>[^/]+).csv', '\\g<title>.csv')
        volume_transformer = VolumeConfig('data2', '/var/doc')
        volume_transformer.transformations = [transformation]

        volumes = [volume_mirror, volume_transformer]

        # Act.
        proxy_factory = ProxyFactory()
        proxies = proxy_factory.create_proxies(volumes)

        # Assert.
        self.assertEqual(2, len(proxies))

        self.assertEqual('/mnt/new_volume', proxies[0].mount_point)
        self.assertIsInstance(proxies[0].fuse_fs.__class__, type(MirrorFs))

        self.assertEqual('/var/doc', proxies[1].mount_point)
        self.assertIsInstance(
            proxies[1].fuse_fs.__class__,
            type(TransformerFs))

    def test_create_proxies_transformers_separate_mount_points(self):
        # Arrange.
        transformation1 = TransformationConfig(
            'dir1/(?P<title>[^/]+).csv', '\\g<title>_1.csv')
        volume1 = VolumeConfig('data1', '/var/doc1')
        volume1.transformations = [transformation1]

        transformation2 = TransformationConfig(
            'dir2/(?P<title>[^/]+).csv', '\\g<title>_2.csv')
        volume2 = VolumeConfig('data2', '/var/doc2')
        volume2.transformations = [transformation2]

        volumes = [volume1, volume2]

        # Act.
        proxy_factory = ProxyFactory()
        proxies = proxy_factory.create_proxies(volumes)

        # Assert.
        self.assertEqual(2, len(proxies))

        self.assertEqual('/var/doc1', proxies[0].mount_point)
        self.assertIsInstance(
            proxies[0].fuse_fs.__class__,
            type(TransformerFs))

        self.assertEqual('/var/doc2', proxies[1].mount_point)
        self.assertIsInstance(
            proxies[1].fuse_fs.__class__,
            type(TransformerFs))

    def test_create_proxies_transformers_same_mount_point(self):
        # Arrange.
        transformation1 = TransformationConfig(
            'dir1/(?P<title>[^/]+).csv', '\\g<title>_1.csv')
        volume1 = VolumeConfig('data1', '/var/doc')
        volume1.transformations = [transformation1]

        transformation2 = TransformationConfig(
            'dir2/(?P<title>[^/]+).csv', '\\g<title>_2.csv')
        volume2 = VolumeConfig('data2', '/var/doc')
        volume2.transformations = [transformation2]

        volumes = [volume1, volume2]

        # Act.
        proxy_factory = ProxyFactory()
        proxies = proxy_factory.create_proxies(volumes)

        # Assert.
        self.assertEqual(1, len(proxies))

        self.assertEqual('/var/doc', proxies[0].mount_point)
        self.assertIsInstance(
            proxies[0].fuse_fs.__class__,
            type(TransformerFs))
