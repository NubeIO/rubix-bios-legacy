from flask import Blueprint
from flask_restful import Api

from src.service.resources.control import ServiceControl
from src.service.resources.token import TokenResource
from src.service.resources.upgrade import UpgradeResource, ReleaseResource, UpdateCheckResource, UploadUpgradeResource
from src.system.resources.ping import Ping
from src.users.resource_login_users import UsersLoginResource
from src.users.resource_users import UsersResource

bp_service = Blueprint('service', __name__, url_prefix='/api/service')
api_service = Api(bp_service)
api_service.add_resource(UpgradeResource, '/upgrade')
api_service.add_resource(UploadUpgradeResource, '/upload_upgrade')
api_service.add_resource(TokenResource, '/token')
api_service.add_resource(ReleaseResource, '/releases')
api_service.add_resource(UpdateCheckResource, '/update_check')
api_service.add_resource(ServiceControl, '/control')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(Ping, '/ping')

bp_users = Blueprint('users', __name__, url_prefix='/api/users')
api_users = Api(bp_users)
api_users.add_resource(UsersResource, '')
api_users.add_resource(UsersLoginResource, '/login', endpoint="login")
