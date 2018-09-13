"""
Makara Website
Live development toool
author: hugh@blinkybeach.com
copyright: Blinky Beach Pty Ltd
"""
import os
from pathlib import Path
import time
# Overrides builtin compile reserved word. Acceptable given the narrow, limited
# scope of this tool.
from compile import compile
from datetime import datetime

LOG_DATE_FORMAT = '%H:%M:%S'

class WatchedFile:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._modified_time = os.path.getmtime(filepath)
        return

    def was_deleted(self) -> bool:
        path = Path(self._filepath)
        if not path.is_file():
            return True
        return False

    def has_changed(self) -> bool:
        if self.was_deleted():
            return True
        latest_modified_time = os.path.getmtime(self._filepath)
        if latest_modified_time > self._modified_time:
            self._modified_time = latest_modified_time
            return True
        return False

class Directory:
    def __init__(self, path: str):
        self._raw_path = path
        self._files = None
        self._directories = None
        self._refresh_contents()
        self._last_item_count = self._count_contents()
        return

    def was_deleted(self) -> bool:
        path = Path(self._raw_path)
        if not path.is_dir():
            return True
        return False

    def has_changed(self) -> bool:
        if self._has_changed():
            self._refresh_contents()
            self._last_item_count = self._count_contents()
            return True
        return False

    def _has_changed(self) -> bool:
        if self.was_deleted():
            return True
        if self._count_contents() != self._last_item_count:
            return True
        if self._files is not None:
            if True in [f.has_changed() for f in self._files]:
                return True
        if self._directories is not None:
            if True in [d.has_changed() for d in self._directories]:
                return True
        return False

    def _refresh_contents(self) -> None:
        path = self._raw_path
        raw_contents = os.listdir(path)
        contents = [(path + '/' + c) for c in raw_contents]
        filenames = [f for f in contents if os.path.isfile(f)]
        self._files = [WatchedFile(f) for f in filenames]
        directories = [Directory(f) for f in contents if not os.path.isfile(f)]
        self._directories = directories
        return

    def _count_contents(self) -> int:
        contents = os.listdir(self._raw_path)
        return len(contents)

class Snapshot:
    def __init__(self, directories: [str], files: [str]):
        self._directories = [Directory(n) for n in directories]
        self._files = [WatchedFile(f) for f in files]
        return

    def has_changed(self) -> bool:
        if True in [d.has_changed() for d in self._directories]:
            return True
        if True in [f.has_changed() for f in self._files]:
            return True
        return False

SNAPSHOT = Snapshot(
    ('javascript', 'styles'),
    ('template.html', 'analytics.js')
)

def log_prefix() -> str:
    now = datetime.now()
    log_str_prefix = '[' + now.strftime(LOG_DATE_FORMAT) + '] '
    return log_str_prefix

print(log_prefix() + 'Watching for changes in site source files')
compile(debug=True)
while True:
    if SNAPSHOT.has_changed():
        log_str = log_prefix()
        log_str += 'Detected change, recompiling index.html'
        print(log_str)
        compile(debug=True)
    time.sleep(0.2)
