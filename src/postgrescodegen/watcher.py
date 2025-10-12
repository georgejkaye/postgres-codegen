import time

from datetime import datetime, timedelta
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from postgrescodegen.processor import process_all_script_files


class WatcherHandler(FileSystemEventHandler):
    def __init__(
        self,
        internal_scripts_path: Path,
        user_scripts_path: Path,
        output_package_dir: Path,
        output_module_name: str,
        roll_scripts: bool,
    ):
        self.last_trigger_time = datetime.now()
        self.internal_scripts_path = internal_scripts_path
        self.user_scripts_path = user_scripts_path
        self.output_package_dir = output_package_dir
        self.output_module_name = output_module_name
        self.roll_scripts = roll_scripts

    def process_script_files_if_appropriate(self):
        current_time = datetime.now()
        if (current_time - self.last_trigger_time) > timedelta(seconds=1):
            process_all_script_files(
                self.internal_scripts_path,
                self.user_scripts_path,
                self.output_package_dir,
                self.output_module_name,
                self.roll_scripts,
            )

    def on_created(self, event: FileSystemEvent):
        self.process_script_files_if_appropriate()

    def on_modified(self, event: FileSystemEvent):
        self.process_script_files_if_appropriate()

    def on_moved(self, event: FileSystemEvent):
        self.process_script_files_if_appropriate()


def start_watcher(
    internal_scripts_path: Path,
    user_scripts_path: Path,
    output_package_dir: Path,
    output_module_name: str,
    roll_scripts: bool,
):
    event_handler = WatcherHandler(
        internal_scripts_path,
        user_scripts_path,
        output_package_dir,
        output_module_name,
        roll_scripts,
    )
    observer = Observer()
    observer.schedule(event_handler, str(user_scripts_path), recursive=True)
    observer.start()
    print(f"Watching script files in: {user_scripts_path}", flush=True)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
