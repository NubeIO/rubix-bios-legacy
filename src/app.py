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

    def register_router(_app) -> Flask:
        from src.routes import bp_bios, bp_system
        _app.register_blueprint(bp_bios)
        _app.register_blueprint(bp_system)
        return _app

    return register_router(app)
