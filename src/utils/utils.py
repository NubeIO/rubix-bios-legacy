import enum

from flask_restful import abort


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
    return f"sudo systemctl {action} {service_file_name}".strip()
