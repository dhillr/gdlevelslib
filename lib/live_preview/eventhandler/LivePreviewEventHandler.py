import subprocess
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from gdlevelslib import GJPreviewPathS

class LivePreviewEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"[LOG] Server restarting! ({event.src_path} was modified)")
        subprocess.run(["python", "-m", "http.server", "8000"])

if __name__ == "__main__":
    event_handler = LivePreviewEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=GJPreviewPathS, recursive=True)
    observer.start()

    print("[LOG] Server started! (http://localhost:8000/lib/live_preview/index.html)")
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()