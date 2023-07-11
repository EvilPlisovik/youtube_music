import os.path
from os.path import join, dirname, abspath
import pytest

path_to_files = abspath(join(dirname(__file__), 'music'))


def test_invalid_path():
    # with pytest.raises(OSError):
        ...