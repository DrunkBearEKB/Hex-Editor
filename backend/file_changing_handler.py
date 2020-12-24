import time
from watchdog.events import FileSystemEventHandler


class FileChangingHandler(FileSystemEventHandler):
    def __init__(self, hex_editor, file_name):
        super().__init__()
        self._hex_editor = hex_editor
        self._file_name = file_name

    def on_modified(self, event):
        if event.src_path.replace('\\', '/') == self._file_name:
            time.sleep(0.005)
            self._hex_editor.update_all(direction=0)
