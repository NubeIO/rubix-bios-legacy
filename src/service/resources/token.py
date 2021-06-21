from flask_restful import Resource, reqparse, abort
from registry.models.model_github_info import GitHubInfoModel
from registry.resources.resource_github_info import put_github_info, get_github_info


class TokenResource(Resource):

    @classmethod
    def get(cls):
        github_info_model: [GitHubInfoModel, None] = get_github_info()
        if not github_info_model:
            abort(404, message="GitHub token doesn't exist")
        return {"token": f"***{github_info_model.token[-4:]}"}

    @classmethod
    def put(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        args = parser.parse_args()
        token: str = args['token']
        put_github_info(GitHubInfoModel(token=token))
        return {'token': get_github_info().token}
