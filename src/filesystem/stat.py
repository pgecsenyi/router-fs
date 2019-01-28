import os
from datetime import datetime


# pylint: disable=too-many-instance-attributes
class Stat:

    default_gid = os.getgid()
    default_time = datetime.timestamp(datetime.now())
    default_uid = os.getuid()

    def __init__(self):
        self.st_atime = 0
        self.st_ctime = 0
        self.st_gid = 0
        self.st_mode = 0
        self.st_mtime = 0
        self.st_nlink = 0
        self.st_size = 0
        self.st_uid = 0

    @staticmethod
    def create_default(is_file=False):
        stat = Stat()

        stat.st_atime = Stat.default_time
        stat.st_ctime = Stat.default_time
        stat.st_gid = Stat.default_gid
        stat.st_mode = 16877
        if is_file:
            stat.st_mode = 33188

        stat.st_mtime = Stat.default_time
        stat.st_nlink = 2
        stat.st_size = 4096
        stat.st_uid = Stat.default_uid

        return stat
