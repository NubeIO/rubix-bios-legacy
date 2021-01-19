from flask import Blueprint
from flask_restful import Api

from src.bios.resources.bios import UpgradeResource
from src.system.resources.ping import Ping

bp_bios = Blueprint('bios', __name__, url_prefix='/api/bios')
api_bios = Api(bp_bios)
api_bios.add_resource(UpgradeResource, '/upgrade')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(Ping, '/ping')
