from threading import Thread, RLock
from queue import Queue
from pytube.exceptions import VideoUnavailable


lock = RLock()


class LoadersTread(Thread):

    def __init__(self, save_path: str, file_name: str, tasks: Queue, errors: Queue):
        Thread.__init__(self)
        self._tasks = tasks
        self._errors = errors
        self._save_path = save_path
        self._file_name = file_name

    def run(self):
        while True:
            if self._tasks.empty():
                break

            task = self._tasks.get()
            try:
                task(output_path=self._save_path, filename=self._file_name)
            except VideoUnavailable as e:
                self._errors.put(e.error_string())
            with lock:
                self._tasks.task_done()




