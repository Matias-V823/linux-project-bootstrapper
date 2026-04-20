import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DESTINO = "/home/matias/Desktop/projects"
EXTENSIONES_VALIDAS = (".js", ".tsx", ".py", ".ts", ".jsx")

def carpeta_tiene_archivos_validos(carpeta):
    for nombre in os.listdir(carpeta):
        if nombre.endswith(EXTENSIONES_VALIDAS):
            return True
    return False

def archivo_creado(event):
    if event.is_directory:
        return

    if not event.src_path.endswith(EXTENSIONES_VALIDAS):
        return

    carpeta_origen = os.path.dirname(event.src_path)
    nombre_carpeta = os.path.basename(carpeta_origen)
    ruta_destino = os.path.join(DESTINO, nombre_carpeta)

    if os.path.exists(ruta_destino):
        print(f"La carpeta ya existe en destino: {ruta_destino}")
        return

    if not carpeta_tiene_archivos_validos(carpeta_origen):
        print(f"No hay archivos válidos en: {carpeta_origen}")
        return

    shutil.move(carpeta_origen, ruta_destino)
    print(f"Carpeta movida a: {ruta_destino}")

handler = FileSystemEventHandler()
handler.on_created = archivo_creado

observer = Observer()
observer.schedule(handler, ".", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()