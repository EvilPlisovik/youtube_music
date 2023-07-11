import os.path
import os
from loader.setting import OptionSave
from loader.music_download import MusicDownload
from pytube import YouTube
from pytube.exceptions import PytubeError


class FilesManager:

    def __init__(self, options: OptionSave, loader: MusicDownload):
        self._save_path = options.save_path
        self._is_directory = True if options.save_directory == 'yes' else False
        self._is_zip = options.is_zip
        self._name_directory = options.name_directory
        self._loader = loader

    def save(self, url: str) -> dict[str, list[str]]:
        try:
            yt = YouTube(url)
        except PytubeError:
            return {'error': ['Not valid url!']}

        if self._is_directory:
            full_path = self._get_save_path(yt)
            if not os.path.exists(full_path):
                try:
                    os.mkdir(full_path)
                except OSError:
                    return {'error': ['Directory cannot be created or invalid path!']}
        else:
            full_path = self._save_path
            if not os.path.exists(full_path):
                return {'error': ['Invalid path!']}
        return self._loader.download(full_path, yt.title, yt.streams)

    def _get_save_path(self, yt: YouTube) -> str:
        match self._name_directory:
            case 'author':
                name_directory = yt.author
            case 'title':
                name_directory = yt.title
            case _:
                name_directory = self._name_directory

        return os.path.join(self._save_path, name_directory)
