from flask import Blueprint
from flask_restful import Api

from src.service.resources.service import UpgradeResource
from src.service.resources.token import TokenResource
from src.system.resources.ping import Ping

bp_service = Blueprint('service', __name__, url_prefix='/api/service')
api_service = Api(bp_service)
api_service.add_resource(UpgradeResource, '/upgrade')
api_service.add_resource(TokenResource, '/token')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(Ping, '/ping')
