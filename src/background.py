import logging
import time
from typing import Union

import gevent
from flask import current_app
from gevent import sleep

from src.handlers.exception import exception_handler
from src.restart_registry import RestartRegistry
from src.service.models.model_systemd import RubixServiceSystemd
from src.service.models.model_upgrade import UpgradeModel, AppState
from src.service.resources.upgrade import download, REPO_NAME, install, get_latest_release, get_release_link, \
    get_installed_app_version
from src.setting import AppSetting
from src.utils.shell import systemctl_is_active_service_state
from src.utils.utils import get_github_token

logger = logging.getLogger(__name__)

REITERATION_TIME_SEC: int = 20
RE_DOWNLOAD_TIME_SEC: int = 300
WAIT_AFTER_RESTART: int = 60
MAX_BLOCKED_ITERATION: int = 60

download_start_time: Union[float, None] = None
blocked_iteration_count: int = 0


class Background:
    @staticmethod
    def run():
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        if setting.prod:
            gevent.spawn(check_and_upgrade_app, current_app._get_current_object().app_context)


def check_and_upgrade_app(app_context):
    with app_context():
        while True:
            logger.info("Looping has been started ---------------------")
            check_and_upgrade_app_loop()
            logger.info("End of looping -------------------------------")
            sleep(REITERATION_TIME_SEC)


@exception_handler
def check_and_upgrade_app_loop():
    global blocked_iteration_count
    app_state: AppState = UpgradeModel.get_app_state()
    if app_state == AppState.BLOCKED:
        if blocked_iteration_count >= MAX_BLOCKED_ITERATION:
            logger.info(f"We did {blocked_iteration_count} iterations and it's still blocked, so unblocking it!")
            UpgradeModel.update_app_state(AppState.FINISHED)
        logger.info(f"App state is blocked, count={blocked_iteration_count}!")
        blocked_iteration_count += 1
        return
    token: str = get_github_token()
    blocked_iteration_count = 0
    if app_state == AppState.STARTED:
        logger.info(f'App upgrade state: {app_state.name}')
        version: str = get_latest_release(get_release_link(REPO_NAME), token)
        logger.info(f"We are started to download/install latest version: {version}")
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
                logger.info(f"We are started to download/install latest version: {version}")
                version = get_latest_release(get_release_link(REPO_NAME), token)
            else:
                logger.info(f"We are started to download/install existing version: {version}")
            installation: bool = download_and_install_app(version, token)
            logger.info(f'Installation state: {{"version": {version}, "installation:" {installation}}}')
            if not installation:
                return
        UpgradeModel.update_app_state(AppState.FINISHED)
    else:
        logger.info(f'App upgrade state: {app_state.name}')
        if RestartRegistry().restarted:
            RestartRegistry().set_restart_state(False)
            logger.info(f"We are waiting {WAIT_AFTER_RESTART} seconds coz restart function has been called...")
            sleep(WAIT_AFTER_RESTART)
        is_active: bool = systemctl_is_active_service_state(RubixServiceSystemd.SERVICE_FILE_NAME)
        logger.info(f'App state: {is_active}')
        if not is_active:
            UpgradeModel.update_app_state(AppState.RUNNING)


def download_and_install_app(_version, token) -> bool:
    app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
    global download_start_time
    try:
        should_download: bool = False
        if download_start_time is None:
            download_start_time = time.time()
            should_download = True
            logger.info("Download process has been started...")
        elif time.time() - download_start_time >= RE_DOWNLOAD_TIME_SEC:
            should_download = True
            download_start_time = time.time()
            logger.info("Re-download process has been started...")
        else:
            time_diff: str = "{:.2f}".format(time.time() - download_start_time)
            logger.info(f"We skipped download process coz re-download time difference is: {time_diff} seconds")
        if should_download:
            download(app_setting, REPO_NAME, _version, token)
        logger.info("Installation process has been started...")
        return install(app_setting, REPO_NAME, _version)
    except Exception as e:
        logger.error(str(e))
        return False
