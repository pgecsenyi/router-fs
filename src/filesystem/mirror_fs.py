import errno
import os

from fuse import FuseOSError, Operations

# pylint: disable=unused-import
from util.decorate_all import decorate_all, dont_decorate
from util.log_decorator import log_decorator


# pylint: disable=too-many-public-methods
class MirrorFs(Operations, metaclass=decorate_all(log_decorator)):

    def __init__(self, root):
        self._root = root

    ####################################################################################################################
    # Methods related to directory and permission mangement.
    ####################################################################################################################

    def access(self, path, amode):
        full_path = self._full_path(path)
        if not os.access(full_path, amode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        stat = os.lstat(full_path)
        attrs = ('st_atime', 'st_ctime', 'st_gid', 'st_mode',
                 'st_mtime', 'st_nlink', 'st_size', 'st_uid')
        return dict((key, getattr(stat, key)) for key in attrs)

    def link(self, target, source):
        return os.link(self._full_path(target), self._full_path(source))

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for entry in dirents:
            yield entry

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self._root)
        return pathname

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        attrs = (
            'f_bavail', 'f_bfree', 'f_blocks', 'f_bsize',
            'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax')
        return dict((key, getattr(stv, key)) for key in attrs)

    def symlink(self, target, source):
        return os.symlink(source, self._full_path(target))

    def unlink(self, path):
        return os.unlink(self._full_path(path))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    ####################################################################################################################
    # Methods related to file management.
    ####################################################################################################################

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def flush(self, path, fh):
        return os.fsync(fh)

    def fsync(self, path, datasync, fh):
        return self.flush(path, fh)

    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def read(self, path, size, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, size)

    def release(self, path, fh):
        return os.close(fh)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as opened_file:
            opened_file.truncate(length)

    def write(self, path, data, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, data)

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self._root, partial)
        return path
