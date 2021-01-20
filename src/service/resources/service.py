import json
import os
import shutil
from urllib.error import HTTPError

import requests
from flask import current_app
from flask_restful import Resource, abort
from packaging import version

from src.service.systemd import RubixServiceSystemd, Systemd
from src.setting import AppSetting
from src.system.utils.file import download_unzip_service, delete_existing_folder


class UpgradeResource(Resource):
    @classmethod
    def get(cls):
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        try:
            repo_name: str = 'rubix-service'
            _version: str = _get_latest_release(_get_release_link(repo_name))
            download(app_setting, repo_name, _version)
            installation = install(app_setting, repo_name, _version)
            return {
                'installation': installation
            }
        except Exception as e:
            abort(501, message=str(e))


def download(app_setting: AppSetting, repo_name: str, _version: str):
    download_dir = _get_download_dir(app_setting, repo_name)
    download_link: str = _get_download_link(repo_name, _version, app_setting.device_type)
    delete_existing_folder(download_dir)
    try:
        name: str = download_unzip_service(download_link, download_dir, None)  # todo token
    except HTTPError as e:
        raise HTTPError(e.url, e.code, 'download link or token might have error', e.headers, e.fp)
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
    systemd: Systemd = RubixServiceSystemd(installed_dir, app_setting.device_type)
    installation = systemd.install()
    delete_existing_folder(downloaded_dir)
    return installation


def _get_latest_release(releases_link: str):
    resp = requests.get(releases_link)
    data = json.loads(resp.content)
    latest_release = ''
    for row in data:
        release = row.get('tag_name')
        if not latest_release or version.parse(latest_release) <= version.parse(release):
            latest_release = release
    return latest_release


def _get_download_link(repo_name: str, _version: str, device_type: str) -> str:
    release_link = 'https://api.github.com/repos/NubeIO/{}/releases/tags/{}'.format(repo_name, _version)
    resp = requests.get(release_link)
    row = json.loads(resp.content)
    for asset in row.get('assets', []):
        if device_type in asset.get('browser_download_url'):
            return asset.get('browser_download_url')
    raise ModuleNotFoundError('No app for type {} & version {}'.format(device_type, _version))


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
