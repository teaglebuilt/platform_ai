from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from platform_ai.domain.ports.handler import EventHandler


class FileSystemObserver:
    def __init__(self, path: Path, handler: EventHandler):
        self.path = path
        self.handler = self.WatchdogHandler(handler)
        self.observer = Observer()

    class WatchdogHandler(FileSystemEventHandler):
        def __init__(self, handler: EventHandler):
            self.handler = handler

        def on_modified(self, event: FileSystemEvent):
            if not event.is_directory:
                self.handler.handle_event("file_modified", {"path": event.src_path})

    def add_watch(self, path: Path, handler: EventHandler):
        print(f"👀 Watching {path} for changes...")
        self.observer.schedule(self.handler, path=str(path), recursive=False)
        # self.projects.append((path, handler))

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
