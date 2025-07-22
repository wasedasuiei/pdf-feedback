import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = "/Users/tsukarintaro/Desktop/feedback"  # ←このままでOK

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".pdf"):
            print(f"[INFO] 新しいPDFを検出: {event.src_path}")
            # 次のステップ：Firebaseアップロード予定

if __name__ == "__main__":
    print(f"📂 フォルダ監視を開始します: {WATCH_FOLDER}")
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

