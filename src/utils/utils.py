import enum
from typing import Union

from flask_restful import abort
from registry.models.model_github_info import GitHubInfoModel
from registry.resources.resource_github_info import get_github_info


class ServiceAction(enum.Enum):
    START = 1
    STOP = 2
    RESTART = 3
    DISABLE = 4
    ENABLE = 5


def validate_and_create_action(action) -> str:
    if action.upper() in ServiceAction.__members__.keys():
        return action.lower()
    abort(404, message='action should be `start | stop | restart | disable | enable`')


def create_service_cmd(action, service_file_name) -> str:
    return f"systemctl {action} {service_file_name}".strip()


def get_github_token() -> str:
    github_info: Union[GitHubInfoModel, None] = get_github_info()
    return github_info.token if github_info else ""
