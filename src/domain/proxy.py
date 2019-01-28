class Proxy:

    def __init__(self, mount_point, fuse_fs, allow_other):
        self.mount_point = mount_point
        self.fuse_fs = fuse_fs
        self.allow_other = allow_other
