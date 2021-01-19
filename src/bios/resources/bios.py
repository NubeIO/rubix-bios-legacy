from flask_restful import Resource


class UpgradeResource(Resource):
    @classmethod
    def get(cls):
        return {}
