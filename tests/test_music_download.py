import os.path
from pytest import mark
from loader.music_download import MusicDownload
from loader.setting import OptionLoader
from conftest import path_to_test_files


@mark.single
def test_single_download_without_environment(clear, obj_youtube):
    MusicDownload(OptionLoader('all', 'ignored'), 'no').download(path_to_test_files,
                                                                 'test',
                                                                 obj_youtube)
    assert len(os.listdir(path_to_test_files)) == 5


@mark.multi
def test_multi_download_with_environment(environment, obj_youtube):
    MusicDownload(environment.get('current_options_loader'),
                  environment.get('is_treads')).download(environment.get('current_options_save').save_path,
                                                         'test',
                                                         obj_youtube)
    assert len(os.listdir(path_to_test_files)) == 5
