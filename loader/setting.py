from os.path import join, dirname, abspath
from collections import namedtuple
from dotenv import dotenv_values, set_key
from dataclasses import dataclass


@dataclass
class OptionLoader:
    streams_music: str
    abr: str


@dataclass
class OptionSave:
    save_path: str
    save_directory: str
    name_directory: str
    is_zip: str


path_to_environment = abspath(join(dirname(__file__), '../.env'))
options_loader = namedtuple('options_loader', 'streams_music abr')
options_save = namedtuple('options_save', 'save_path save_directory name_directory is_zip')


def load_setting() -> dict:
    settings = dotenv_values(path_to_environment)

    current_options_loader = OptionLoader(settings.get('STREAMS_MUSIC'),
                                          settings.get('ABR'))

    current_options_save = OptionSave(settings.get('SAVE_PATH'),
                                      settings.get('SAVE_DIRECTORY'),
                                      settings.get('NAME_DIRECTORY'),
                                      settings.get('IS_ZIP'))

    is_multi = settings.get('MULTIPROCESSING')
    is_treads = settings.get('TREADS')

    return {'current_options_loader': current_options_loader,
            'current_options_save': current_options_save,
            'is_multi': is_multi,
            'is_treads': is_treads}


def set_setting(settings: dict[str, str]):
    for setting, value in settings.items():
        set_key(path_to_environment, setting, value)
