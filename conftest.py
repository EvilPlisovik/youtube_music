from os.path import abspath, join, dirname
import os
from shutil import rmtree
from pytest import fixture
from pytube import YouTube
from pytube import Channel
from loader.setting import load_setting, set_setting, OptionLoader, OptionSave

path_to_test_files = abspath(join(dirname(__file__), r'tests\music'))


def delete_files():
    for name_files in os.listdir(path_to_test_files):
        rmtree(join(path_to_test_files, name_files))


@fixture
def environment():
    old_environment = load_setting()
    set_setting({'TREADS': 'yes',
                 'STREAMS_MUSIC': 'all',
                 'ABR': 'ignored',
                 'SAVE_PATH': path_to_test_files})

    yield load_setting()

    old_options_loader = old_environment.get('current_options_loader')
    old_options_save = old_environment.get('current_options_save')
    set_setting({'TREADS': old_environment.get('is_treads'),
                 'STREAMS_MUSIC': old_options_loader.abr,
                 'ABR': old_options_loader.streams_music,
                 'SAVE_PATH': old_options_save.save_path})

    delete_files()


@fixture
def clear():
    yield
    delete_files()


@fixture(scope="module")
def obj_youtube():
    return YouTube('https://www.youtube.com/watch?v=eAy2eVlvaZQ').streams


@fixture(scope='module')
def urls():
    channel = Channel('https://www.youtube.com/@Sabaton')
    return channel.video_urls[7:9]


@fixture
def setting():
    current_options_loader = OptionLoader('all', 'ignored')
    current_options_save = OptionSave(path_to_test_files,
                                      'yes',
                                      'title',
                                      'no')
    return {'current_options_loader': current_options_loader,
            'current_options_save': current_options_save,
            'is_multi': False,
            'is_treads': False}
