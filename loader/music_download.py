from multiprocessing import cpu_count
import queue
from loader.setting import OptionLoader
from pytube import StreamQuery, Stream
from pytube.exceptions import VideoUnavailable
from loader.loader_tread import LoadersTread


class MusicDownload:

    def __init__(self, options: OptionLoader, is_treads: str):
        self._streams_music = options.streams_music
        self._abr = options.abr
        self.is_treads = True if is_treads == 'yes' else False

    def download(self, save_path: str, file_name: str, streams: StreamQuery) -> dict[str, list[str]]:

        streams = self._prepare_download(streams)

        if len(streams) > 0:
            if isinstance(streams, Stream):
                return MusicDownload._single_download(streams, save_path, file_name)

            if not self.is_treads:
                errors = []
                for stream in streams:
                    errors.extend(MusicDownload._single_download(stream, save_path, file_name).get('error'))
                return {'error': errors}

            return MusicDownload._multi_treads_download(streams, save_path, file_name)

        return {'error': ['Audio file with current settings not found!']}

    def _prepare_download(self, streams: StreamQuery) -> StreamQuery:
        match self._streams_music:
            case 'best':
                streams = streams.filter(only_audio=True, file_extension='mp4').order_by('abr').last()
            case 'all':
                streams = streams.filter(only_audio=True).order_by('abr')
            case _:
                if self._abr == 'ignored':
                    streams = streams.filter(only_audio=True, file_extension=self._streams_music).order_by('abr')
                else:
                    streams = streams.filter(only_audio=True, file_extension=self._streams_music, abr=self._abr)
        return streams

    @staticmethod
    def _single_download(stream: Stream, save_path: str, file_name: str) -> dict[str, list[str]]:
        try:
            stream.download(output_path=save_path,
                            filename=f"{'_'.join([file_name, stream.abr, stream.audio_codec])}."
                                     f"{stream.mime_type.split('/')[-1]}")
            return {'error': []}
        except VideoUnavailable as e:
            return {'error': [e.error_string()]}


    @staticmethod
    def _multi_treads_download(streams: StreamQuery, save_path: str, file_name: str) -> dict[str, list[str]]:
        tasks = queue.Queue()
        errors = queue.Queue()
        num_cpu = cpu_count()
        if num_cpu > len(streams):
            num_cpu = len(streams)

        loaders = [LoadersTread(save_path,
                                f"{'_'.join([file_name, streams[i].abr, streams[i].audio_codec])}."
                                f"{streams[i].mime_type.split('/')[-1]}",
                                tasks,
                                errors) for i in range(num_cpu)]

        for stream in streams:
            tasks.put(stream.download)

        for loader in loaders:
            loader.start()
        for loader in loaders:
            loader.join()

        if errors.qsize() > 0:
            return {'error': [errors.get() for _ in range(errors.qsize())]}
        return {'error': []}
