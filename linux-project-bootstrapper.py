import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DESTINATION = "/home/matias/Desktop/projects"
VALID_EXTENSIONS = (".js", ".tsx", ".py", ".ts", ".jsx", ".json")
DOCKER_DESTINATION = "/home/matias/Desktop/docker"
PROCESSED_FOLDERS = set()

def get_root_folder(path):
    """Get the root folder of the project by searching for package.json"""
    folder = os.path.dirname(path)
    
    while folder != "/" and not os.path.exists(os.path.join(folder, "package.json")):
        parent = os.path.dirname(folder)
        if parent == folder:  
            break
        folder = parent
    
    return folder

def folder_has_valid_files(folder):
    """Check if folder contains files with valid extensions"""
    if not os.path.exists(folder):
        return False
    try:
        for filename in os.listdir(folder):
            if filename.endswith(VALID_EXTENSIONS):
                return True
    except:
        return False
    return False

def on_file_created(event):
    """Handler for file creation events"""
    if event.is_directory:
        return

    if not event.src_path.endswith(VALID_EXTENSIONS):
        return

    root_folder = get_root_folder(event.src_path)
    folder_name = os.path.basename(root_folder)
    destination_path = os.path.join(DESTINATION, folder_name)
    docker_path = os.path.join(DOCKER_DESTINATION, folder_name)

    if folder_name in PROCESSED_FOLDERS:
        return

    if not os.path.exists(root_folder):
        return

    if os.path.exists(destination_path):
        print(f"Folder already exists in destination: {destination_path}")
        PROCESSED_FOLDERS.add(folder_name)
        return

    if not folder_has_valid_files(root_folder):
        return

    try:
        shutil.move(root_folder, destination_path)
        os.makedirs(docker_path, exist_ok=True)
        PROCESSED_FOLDERS.add(folder_name)
        print(f"Project moved to: {destination_path}")
        print(f"Folder created in docker: {docker_path}")
    except Exception as e:
        print(f"Error moving folder: {e}")

handler = FileSystemEventHandler()
handler.on_created = on_file_created

observer = Observer()
observer.schedule(handler, ".", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()