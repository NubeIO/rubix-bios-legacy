from flask import current_app
from flask_restful import Resource, abort

from src.service.resources.service import _get_latest_release, _get_release_link, _get_installation_dir
from src.setting import AppSetting
from src.system.utils.file import get_extracted_dir


class UpdateCheckResource(Resource):
    @classmethod
    def get(cls):
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        try:
            repo_name: str = 'rubix-service'
            token: str = app_setting.token
            latest_version: str = _get_latest_release(_get_release_link(repo_name), token)
            installed_version: str = get_extracted_dir(_get_installation_dir(app_setting, repo_name)).split("/")[-1]
            return {
                'latest_version': latest_version,
                'installed_version': installed_version,
                'update_required': latest_version != installed_version
            }
        except Exception as e:
            abort(501, message=str(e))
