import enum
from typing import List

from flask import current_app

from src.setting import AppSetting, BaseSetting
from src.system.utils.file import write_file, read_file


class States(enum.Enum):
    """
    Available unit active states list of systemctl, `systemctl --state=help`.
    """
    ACTIVE = 'active'
    RELOADING = 'reloading'
    INACTIVE = 'inactive'
    FAILED = 'failed'
    ACTIVATING = 'activating'
    DEACTIVATING = 'deactivating'
    MAINTENANCE = 'maintenance'


class AppState(enum.Enum):
    STARTED = 1
    RUNNING = 2
    FINISHED = 3


class AppModel(BaseSetting):
    def __init__(self):
        self.version = ""
        self.service = ""
        self.is_installed = False
        self.state = States.INACTIVE.name
        self.status = False
        self.upgrade_state = AppState.FINISHED.name
        self.date_since = ""
        self.time_since = ""


class UpgradeModel:
    @classmethod
    def update_app_state(cls, app_state: AppState):
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        write_file(app_setting.app_state_file, app_state.name)

    @classmethod
    def get_app_state(cls) -> AppState:
        app_setting = current_app.config[AppSetting.FLASK_KEY]
        app_state: str = read_file(app_setting.app_state_file)
        app_states: List[str] = list(map(lambda a: a.name, AppState))
        if app_state in app_states:
            return AppState[app_state]
        return AppState.FINISHED
