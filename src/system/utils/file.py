import os
import shutil
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen, Request
from zipfile import ZipFile


def delete_existing_folder(dir_) -> bool:
    dir_path = Path(dir_)
    if dir_path.exists() and dir_path.is_dir():
        shutil.rmtree(dir_)
        return True
    return False


def download_unzip_service(download_link, directory, token) -> str:
    req = Request(download_link)
    if token:
        req.add_header("Authorization", "token {}".format(token))
    with urlopen(req) as zip_resp:
        with ZipFile(BytesIO(zip_resp.read())) as z_file:
            z_file.extractall(directory)
            return z_file.namelist()[0]


def write_file(file, content):
    f = open(file, "w")
    f.write(content)
    f.close()


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)
