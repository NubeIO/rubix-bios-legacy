from flask_restful import reqparse, Resource, abort

from src.service.models.model_upgrade import UpgradeModel, AppState
from src.utils.shell import execute_command_with_exception
from src.utils.utils import validate_and_create_action, create_service_cmd


class ServiceControl(Resource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('action',
                            type=str,
                            help='action should be `start | stop | restart | disable | enable`',
                            required=True)
        args = parser.parse_args()
        action: str = validate_and_create_action(args['action'])
        if action == 'restart':
            UpgradeModel.update_app_state(AppState.BLOCKED)
        service_cmd: str = create_service_cmd(action, 'nubeio-rubix-service.service')
        try:
            execute_command_with_exception(service_cmd)
        except Exception as e:
            abort(500, message=str(e))
        finally:
            UpgradeModel.update_app_state(AppState.FINISHED)
        return {}
