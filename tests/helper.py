import pathlib


def get_test_path_of_file(in_file):
    return pathlib.Path(in_file).parent.resolve()
