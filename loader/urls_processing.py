from multiprocessing import JoinableQueue, Queue, cpu_count

from loader.files_manager import FilesManager
from loader.music_download import MusicDownload
from loader.url_process import UrlProcess


class UrlsProcessing:

    def __init__(self, is_multi: bool, setting: dict):
        self._is_multi = is_multi
        self._setting = setting

    def downloads(self, urls: list[str]) -> dict[str, list[str]]:
        if len(urls) < 2:
            return {'error': self._single_download(urls[0])}

        if not self._is_multi:
            errors = []
            for url in urls:
                errors.extend(self._single_download(url))
            return {'error': errors}
        else:
            return self._multi_downloads(urls)

    def _single_download(self, url: str) -> list[str]:
        current_options_save = self._setting.get('current_options_save')
        current_options_save.name_directory = 'title'
        manger = FilesManager(current_options_save,
                              MusicDownload(self._setting.get('current_options_loader'),
                                            (self._setting.get('is_treads'))))
        return manger.save(url).get('error')

    def _multi_downloads(self, urls: list[str]) -> dict[str, list[str]]:

        tasks = JoinableQueue()
        errors = Queue()
        num_cpu = cpu_count()
        if num_cpu > len(urls):
            num_cpu = len(urls)

        processes = [UrlProcess(self._setting, tasks, errors) for _ in range(num_cpu)]

        for url in urls:
            tasks.put(url)

        for _ in range(num_cpu):
            tasks.put(None)

        for process in processes:
            process.start()

        tasks.join()

        if errors.qsize() > 0:
            all_errors = []
            for _ in range(errors.qsize()):
                all_errors.extend(errors.get())
            return {'error': all_errors}
        return {'error': []}
