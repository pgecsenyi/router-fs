from domain import exceptions
from domain.proxy import Proxy
from filesystem.mirror_fs import MirrorFs
from filesystem.transformer_fs import TransformerFs
from filesystem.transformation.directory_lister import DirectoryLister
from filesystem.transformation.transformer import Transformer


class ProxyFactory:

    def create_proxies(self, volumes):
        volumes_by_mount_points = self._group_by_mount_points(volumes)
        proxies = self._build_proxies(volumes_by_mount_points)

        return proxies

    def _group_by_mount_points(self, volumes):
        volumes_by_mount_points = {}
        mount_points_with_mirrors = set()

        for volume in volumes:
            mount_point = volume.mount_point

            if mount_point in mount_points_with_mirrors:
                raise exceptions.InvalidConfigException(
                    'A mount point can only have one volume without transformations (a '
                    'mirror) or several volumes with transformations.')

            volumes_by_mount_points.setdefault(mount_point, [])
            volumes_by_mount_points[mount_point].append(volume)

            if not volume.transformations:
                mount_points_with_mirrors.add(mount_point)

        return volumes_by_mount_points

    def _build_proxies(self, volumes_by_mount_points):
        proxies = []
        for mount_point, volumes in volumes_by_mount_points.items():
            fuse_fs = self._create_fs(volumes)
            allow_other = all(v.allow_other for v in volumes)
            proxy = Proxy(mount_point, fuse_fs, allow_other)
            proxies.append(proxy)

        return proxies

    def _create_fs(self, volumes):
        if len(volumes) > 1 or volumes[0].transformations:
            transformer = self._build_transformer(volumes)
            return TransformerFs(transformer)

        return MirrorFs(volumes[0].source_path)

    def _build_transformer(self, volumes):
        transformer = Transformer()
        for volume in volumes:
            if volume.transformations:
                directory_lister = DirectoryLister(volume.source_path)
                transformer.add_to_cache(
                    directory_lister,
                    volume.transformations)

        return transformer
