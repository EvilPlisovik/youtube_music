import os
from os.path import isdir, join
from pytest import mark
from loader.urls_processing import UrlsProcessing
from conftest import path_to_test_files


def get_list_files(path_to_directory: str):
    list_files = []
    for name in os.listdir(path_to_directory):
        path = join(path_to_directory, name)
        if isdir(path):
            list_files.extend(get_list_files(path))
        else:
            list_files.append(path)
    return list_files


@mark.single
def test_single_downloads_on_urls_channel(clear, urls, setting):
    loader = UrlsProcessing(False, setting)
    loader.downloads(urls)
    assert len(get_list_files(path_to_test_files)) == 10


@mark.multi
def test_multi_downloads_on_urls_channel(clear, urls, setting):
    setting['is_multi'] = True
    setting['is_treads'] = True

    loader = UrlsProcessing(True, setting)
    loader.downloads(urls)
    assert len(get_list_files(path_to_test_files)) == 10
