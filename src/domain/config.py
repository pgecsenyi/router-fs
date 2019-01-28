class Config:

    def __init__(self):
        self.logging = LoggingConfig()
        self.volumes = []


class LoggingConfig:

    def __init__(self):
        self.enabled = False
        self.level = 'error'
        self.max_size_bytes = 524288
        self.path = ''


class VolumeConfig:

    def __init__(self, source_path, mount_point):
        self.source_path = source_path
        self.mount_point = mount_point

        self.allow_other = False
        self.transformations = []


class TransformationConfig:

    def __init__(self, from_path, to_path):
        self.from_path = from_path
        self.to_path = to_path
