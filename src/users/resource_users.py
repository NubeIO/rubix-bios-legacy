from flask import current_app
from flask_restful import Resource, reqparse, marshal_with, abort, fields
from werkzeug.security import generate_password_hash

from src.setting import AppSetting
from src.users.model_users import UserModel


class UsersResource(Resource):
    return_fields = {
        'username': fields.String
    }

    @classmethod
    @marshal_with(return_fields)
    def get(cls):
        user = UserModel.get_user()
        if len(user) == 0:
            abort(404, message='Users not found')
        return user

    @classmethod
    @marshal_with(return_fields)
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        data = parser.parse_args()
        try:
            UserModel.update_user(data['username'], data['password'])
            return UserModel.get_user()
        except Exception as e:
            abort(500, message=str(e))


