from multiprocessing import Process, Queue, JoinableQueue
from loader.files_manager import FilesManager
from loader.music_download import MusicDownload


class UrlProcess(Process):

    def __init__(self, setting: dict, tasks: JoinableQueue, errors: Queue):
        super(UrlProcess, self).__init__()
        self._tasks = tasks
        self._errors = errors
        current_options_save = setting.get('current_options_save')
        current_options_save.name_directory = 'title'
        self._manager = FilesManager(current_options_save,
                                     MusicDownload(setting.get('current_options_loader'),
                                                   (setting.get('is_treads'))))

    def run(self):
        while True:

            url = self._tasks.get()
            if url is None:
                self._tasks.task_done()
                break
            self._errors.put(self._manager.save(url).get('error'))

            self._tasks.task_done()
