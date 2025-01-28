import subprocess
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

p = open(Path.cwd()/"lib"/"live_preview"/"eventhandler"/"path.txt", "r").read()
open(Path.cwd()/"lib"/"live_preview"/"eventhandler"/"path.txt", "w")

class LivePreviewEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(event.event_type, event.src_path)
        # print(f"[LOG] Server restarting! ({event.src_path} was modified)")
        subprocess.run(["python", "-m", "http.server", "8000"])

if __name__ == "__main__":
    eventHandler = LivePreviewEventHandler()
    observer = Observer()
    observer.schedule(eventHandler, path=p, recursive=True)
    observer.start()

    print("[LOG] Server started! (http://localhost:8000/lib/live_preview/index.html)")
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        # observer.stop()
        pass
    observer.join()