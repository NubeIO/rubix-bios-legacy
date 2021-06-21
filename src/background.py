import logging

import gevent
from flask import current_app
from gevent import sleep

from src.handlers.exception import exception_handler
from src.service.models.model_systemd import RubixServiceSystemd
from src.service.models.model_upgrade import UpgradeModel, AppState
from src.service.resources.upgrade import download, REPO_NAME, install, get_latest_release, get_release_link, \
    get_installed_app_version
from src.setting import AppSetting
from src.utils.shell import systemctl_is_active_service_state
from src.utils.utils import get_github_token

logger = logging.getLogger(__name__)


class Background:
    @staticmethod
    def run():
        pass
        gevent.spawn(check_and_upgrade_app, current_app._get_current_object().app_context)


def check_and_upgrade_app(app_context):
    with app_context():
        while True:
            setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
            if setting.prod:
                check_and_upgrade_app_loop()
            sleep(10)


@exception_handler
def check_and_upgrade_app_loop():
    token: str = get_github_token()
    app_state: AppState = UpgradeModel.get_app_state()
    if app_state == AppState.STARTED:
        logger.info(f'App upgrade state: {app_state.name}')
        version: str = get_latest_release(get_release_link(REPO_NAME), token)
        installation: bool = download_and_install_app(version, token)
        if not installation:
            return
        UpgradeModel.update_app_state(AppState.RUNNING)
    elif app_state == AppState.RUNNING:
        logger.info(f'App upgrade state: {app_state.name}')
        is_active: bool = systemctl_is_active_service_state(RubixServiceSystemd.SERVICE_FILE_NAME)
        logger.info(f'App state: {is_active}')
        if not is_active:
            version: str = get_installed_app_version()
            if not version:
                logger.info(f"We are started to install latest version: {version}")
                version = get_latest_release(get_release_link(REPO_NAME), token)
            else:
                logger.info(f"We are started to install existing version: {version}")
            installation: bool = download_and_install_app(version, token)
            logger.info(f'Installation state: {{"version": {version}, "installation:" {installation}}}')
            if not installation:
                return
        UpgradeModel.update_app_state(AppState.FINISHED)
    else:
        logger.info(f'App upgrade state: {app_state.name}')
        is_active: bool = systemctl_is_active_service_state(RubixServiceSystemd.SERVICE_FILE_NAME)
        logger.info(f'App state: {is_active}')
        if not is_active:
            UpgradeModel.update_app_state(AppState.RUNNING)


def download_and_install_app(_version, token) -> bool:
    app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
    try:
        download(app_setting, REPO_NAME, _version, token)
        return install(app_setting, REPO_NAME, _version)
    except Exception:
        return False
