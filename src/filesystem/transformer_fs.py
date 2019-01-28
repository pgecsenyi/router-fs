import errno
import os

from fuse import FuseOSError, Operations

# pylint: disable=unused-import
from filesystem.stat import Stat
from util.decorate_all import decorate_all, dont_decorate
from util.log_decorator import log_decorator


# pylint: disable=too-many-public-methods
class TransformerFs(Operations, metaclass=decorate_all(log_decorator)):

    def __init__(self, transformer):
        self._transformer = transformer

    ####################################################################################################################
    # Methods related to directory and permission mangement.
    ####################################################################################################################

    def access(self, path, amode):
        source_path = self._get_real_path(path)
        if source_path != '':
            if os.access(source_path, amode):
                return 0
        elif amode in (os.R_OK, os.X_OK):
            return 0

        raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        source_path = self._get_real_path(path)
        if source_path != '':
            return os.chmod(source_path, mode)

        raise FuseOSError(errno.EACCES)

    def chown(self, path, uid, gid):
        source_path = self._get_real_path(path)
        if source_path != '':
            return os.chown(source_path, uid, gid)

        raise FuseOSError(errno.EACCES)

    def getattr(self, path, fh=None):
        source_path = self._get_real_path(path)
        if source_path != '':
            stat = os.lstat(source_path)
        else:
            stat = Stat.create_default()

        attrs = ('st_atime', 'st_ctime', 'st_gid', 'st_mode',
                 'st_mtime', 'st_nlink', 'st_size', 'st_uid')

        return dict((key, getattr(stat, key)) for key in attrs)

    def link(self, target, source):
        raise FuseOSError(errno.EACCES)

    def mkdir(self, path, mode):
        raise FuseOSError(errno.EACCES)

    def mknod(self, path, mode, dev):
        raise FuseOSError(errno.EACCES)

    def readdir(self, path, fh):
        entries = ['.', '..']
        file_list = self._transformer.get_directory_contents(path)
        entries.extend(file_list)

        for entry in entries:
            yield entry

    def readlink(self, path):
        full_path = self._get_real_path(path)
        if full_path == '':
            full_path = path

        pathname = os.readlink(full_path)
        if pathname.startswith('/'):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, '/')

        return pathname

    def rename(self, old, new):
        raise FuseOSError(errno.EACCES)

    def rmdir(self, path):
        raise FuseOSError(errno.EACCES)

    def statfs(self, path):
        source_path = self._get_real_path(path)
        if source_path != '':
            stv = os.statvfs(source_path)
            attrs = (
                'f_bavail', 'f_bfree', 'f_blocks', 'f_bsize',
                'f_favail', 'f_ffree', 'f_files', 'f_flag',
                'f_frsize', 'f_namemax')

            return dict((key, getattr(stv, key)) for key in attrs)

        raise FuseOSError(errno.EACCES)

    def symlink(self, target, source):
        raise FuseOSError(errno.EACCES)

    def unlink(self, path):
        raise FuseOSError(errno.EACCES)

    def utimens(self, path, times=None):
        source_path = self._get_real_path(path)
        if source_path != '':
            return os.utime(source_path, times)

        raise FuseOSError(errno.EACCES)

    ####################################################################################################################
    # Methods related to file management.
    ####################################################################################################################

    def create(self, path, mode, fi=None):
        source_path = self._get_real_path(path)
        if source_path != '':
            os.open(source_path, os.O_WRONLY | os.O_CREAT, mode)

        raise FuseOSError(errno.EACCES)

    def flush(self, path, fh):
        return os.fsync(fh)

    def fsync(self, path, datasync, fh):
        source_path = self._get_real_path(path)
        if source_path != '':
            return self.flush(source_path, fh)

        raise FuseOSError(errno.EACCES)

    def open(self, path, flags):
        source_path = self._get_real_path(path)
        if source_path != '':
            return os.open(source_path, flags)

        raise FuseOSError(errno.EACCES)

    def read(self, path, size, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, size)

    def release(self, path, fh):
        return os.close(fh)

    def truncate(self, path, length, fh=None):
        source_path = self._get_real_path(path)
        if source_path != '':
            with open(source_path, 'r+') as opened_file:
                opened_file.truncate(length)

    def write(self, path, data, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, data)

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    @dont_decorate
    def _get_real_path(self, path):
        return self._transformer.get_source_path(path)
