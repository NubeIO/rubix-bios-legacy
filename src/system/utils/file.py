import os
import shutil
from pathlib import Path


def delete_existing_folder(dir_) -> bool:
    dir_path = Path(dir_)
    if dir_path.exists() and dir_path.is_dir():
        shutil.rmtree(dir_)
        return True
    return False


def read_file(file) -> str:
    try:
        with open(file, "r") as f:
            return f.read()
    except Exception:
        return ""


def write_file(file, content):
    f = open(file, "w")
    f.write(content)
    f.close()


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)
