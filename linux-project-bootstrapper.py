import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = "/home/matias"
DESTINATION = "/home/matias/Desktop/projects"
DOCKER_DESTINATION = "/home/matias/Desktop/docker"
VALID_EXTENSIONS = (".js", ".tsx", ".py", ".ts", ".jsx", ".json", ".vue", ".go", ".rs", ".rb")
PROCESSED_FOLDERS = set()

# Folders to ignore (system, hidden, existing)
IGNORED_FOLDERS = {
    "Desktop", "Documents", "Downloads", "Music", "Pictures",
    "Public", "Templates", "Videos", "snap", ".cache", ".config",
    ".local", ".npm", ".nvm", ".ssh", "node_modules", ".git",
    "design_erd", "venv", "__pycache__"
}

def is_direct_child(path):
    """Check if path is a direct child of WATCH_DIR"""
    parent = os.path.dirname(path)
    return parent == WATCH_DIR

def folder_has_valid_files(folder):
    """Recursively check if folder contains files with valid extensions"""
    if not os.path.exists(folder):
        return False
    try:
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if d != "node_modules" and not d.startswith(".")]
            for filename in files:
                if filename.endswith(VALID_EXTENSIONS):
                    return True
    except:
        return False
    return False

def process_folder(folder_path):
    """Process and move the folder if valid"""
    folder_name = os.path.basename(folder_path)
    destination_path = os.path.join(DESTINATION, folder_name)
    docker_folder = os.path.join(DOCKER_DESTINATION, folder_name)
    docker_file_path = os.path.join(docker_folder, "docker-compose.yml")

    if folder_name in PROCESSED_FOLDERS:
        return

    if folder_name in IGNORED_FOLDERS or folder_name.startswith("."):
        return

    if not is_direct_child(folder_path):
        return

    if not os.path.exists(folder_path):
        return

    if os.path.exists(destination_path):
        print(f"Folder already exists in destination: {destination_path}")
        PROCESSED_FOLDERS.add(folder_name)
        return

    if not folder_has_valid_files(folder_path):
        return

    try:
        shutil.move(folder_path, destination_path)
        os.makedirs(docker_folder, exist_ok=True)
        open(docker_file_path, "a").close()

        PROCESSED_FOLDERS.add(folder_name)
        print(f"Project moved to: {destination_path}")
        print(f"docker-compose.yml created at: {docker_file_path}")
    except Exception as e:
        print(f"Error moving folder: {e}")

def on_event(event):
    """Handler for file/directory creation events"""
    if event.is_directory:
        return

    if not event.src_path.endswith(VALID_EXTENSIONS):
        return

    relative = os.path.relpath(event.src_path, WATCH_DIR)
    top_folder = relative.split(os.sep)[0]
    folder_path = os.path.join(WATCH_DIR, top_folder)

    if not os.path.isdir(folder_path):
        return

    time.sleep(2)

    process_folder(folder_path)

handler = FileSystemEventHandler()
handler.on_created = on_event

observer = Observer()
observer.schedule(handler, WATCH_DIR, recursive=True)
observer.start()

print(f"Watching {WATCH_DIR} for new projects...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()