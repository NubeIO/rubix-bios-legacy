import json
import os
import shutil
from io import BytesIO
from zipfile import ZipFile

import requests
from flask import current_app
from flask_restful import Resource, abort, reqparse
from packaging import version

from src.service.systemd import RubixServiceSystemd, Systemd
from src.setting import AppSetting
from src.system.utils.file import delete_existing_folder, get_extracted_dir

REPO_NAME: str = 'rubix-service'


class UpgradeResource(Resource):
    @classmethod
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('version', type=str, required=True)
        args = parser.parse_args()
        _version = args['version']
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        try:
            token: str = app_setting.token
            if _version == "latest":
                _version = _get_latest_release(_get_release_link(REPO_NAME), token)

            download(app_setting, REPO_NAME, _version, token)
            installation = install(app_setting, REPO_NAME, _version)
            return {
                'installation': installation
            }
        except Exception as e:
            abort(501, message=str(e))


class ReleaseResource(Resource):
    @classmethod
    def get(cls):
        try:
            app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
            return _get_releases(_get_release_link(REPO_NAME), app_setting.token)
        except Exception as e:
            abort(501, message=str(e))


class UpdateCheckResource(Resource):
    @classmethod
    def get(cls):
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        try:
            token: str = app_setting.token
            latest_version: str = _get_latest_release(_get_release_link(REPO_NAME), token)
            installed_version: str = get_extracted_dir(_get_installation_dir(app_setting, REPO_NAME)).split("/")[-1]
            return {
                'latest_version': latest_version,
                'installed_version': installed_version,
                'update_required': latest_version != installed_version
            }
        except Exception as e:
            abort(501, message=str(e))


def download(app_setting: AppSetting, repo_name: str, _version: str, token: str):
    download_dir = _get_download_dir(app_setting, repo_name)
    download_link: str = _get_download_link(repo_name, _version, app_setting.device_type, token)
    delete_existing_folder(download_dir)
    try:
        name: str = _download_unzip_service(download_link, download_dir, app_setting.token)
    except Exception:
        raise ModuleNotFoundError(f'download link {download_link} or token might be incorrect')
    extracted_dir: str = os.path.join(download_dir, name)
    dir_with_version: str = os.path.join(download_dir, _version)
    mode: int = 0o744
    os.makedirs(dir_with_version, mode, True)
    app_file: str = os.path.join(dir_with_version, 'app')
    os.rename(extracted_dir, app_file)
    os.chmod(app_file, mode)


def install(app_setting: AppSetting, repo_name: str, _version: str) -> bool:
    installation_dir: str = _get_installation_dir(app_setting, repo_name)
    download_dir: str = _get_download_dir(app_setting, repo_name)
    downloaded_dir: str = _get_downloaded_dir(download_dir, _version)
    installed_dir: str = _get_installed_dir(installation_dir, _version)
    delete_existing_folder(installation_dir)
    shutil.copytree(downloaded_dir, installed_dir)
    systemd: Systemd = RubixServiceSystemd(installed_dir, app_setting.device_type, app_setting.auth)
    installation = systemd.install()
    delete_existing_folder(downloaded_dir)
    return installation


def _get_latest_release(releases_link: str, token: str):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    resp = requests.get(releases_link, headers=headers)
    data = json.loads(resp.content)
    latest_release = ''
    for row in data:
        release = row.get('tag_name', '') if type(row) is dict else ''
        if not latest_release or version.parse(latest_release) <= version.parse(release):
            latest_release = release
    if not latest_release:
        raise ModuleNotFoundError('No version found, check your token & repo')
    return latest_release


def _get_releases(releases_link: str, token: str):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    resp = requests.get(releases_link, headers=headers)
    data = json.loads(resp.content)
    releases = []
    for row in data:
        releases.append(row.get('tag_name'))
    return releases


def _get_download_link(repo_name: str, _version: str, device_type: str, token: str) -> str:
    release_link = 'https://api.github.com/repos/NubeIO/{}/releases/tags/{}'.format(repo_name, _version)
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    resp = requests.get(release_link, headers=headers)
    row = json.loads(resp.content)
    for asset in row.get('assets', []):
        if device_type in asset.get('name'):
            return asset.get('url')
    raise ModuleNotFoundError('No app for type {} & version {}, check your token & repo'.format(device_type, _version))


def _download_unzip_service(download_link, directory, token) -> str:
    headers = {"Accept": "application/octet-stream"}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    r = requests.get(download_link, headers=headers)
    with ZipFile(BytesIO(r.content)) as z_file:
        z_file.extractall(directory)
    return z_file.namelist()[0]


def _get_release_link(repo_name: str) -> str:
    return 'https://api.github.com/repos/NubeIO/{}/releases'.format(repo_name)


def _get_download_dir(app_setting: AppSetting, repo_name: str) -> str:
    return os.path.join(app_setting.download_dir, repo_name)


def _get_installation_dir(app_setting: AppSetting, repo_name: str) -> str:
    return os.path.join(app_setting.install_dir, repo_name)


def _get_downloaded_dir(download_dir: str, _version: str) -> str:
    return os.path.join(download_dir, _version)


def _get_installed_dir(installation_dir: str, _version: str) -> str:
    return os.path.join(installation_dir, _version)
