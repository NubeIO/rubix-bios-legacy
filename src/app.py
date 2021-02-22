import os

from flask import Flask
from flask_cors import CORS

from src.setting import AppSetting


def create_app(app_setting: AppSetting) -> Flask:
    os.environ.setdefault('FLASK_ENV', 'production' if app_setting.prod else 'development')
    app = Flask(__name__)
    app_setting.init_app(app)
    cors = CORS()
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors.init_app(app)

    @app.before_first_request
    def create_default_user():
        from src.users.model_users import UserModel
        UserModel.create_user()

    @app.before_request
    def before_request_fn():
        from src.users.model_users import UserModel
        UserModel.authorize()

    def register_router(_app) -> Flask:
        from src.routes import bp_service, bp_system, bp_users
        _app.register_blueprint(bp_service)
        _app.register_blueprint(bp_system)
        _app.register_blueprint(bp_users)
        return _app

    return register_router(app)
