import os
import pathlib
import shutil


def get_test_path_of_file(in_file):
    return pathlib.Path(in_file).parent.resolve()


def copy_without_permission_bits(src, dst):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    shutil.copyfile(src, dst)


def copy_file(src, dst):
    shutil.copy(src, dst)
