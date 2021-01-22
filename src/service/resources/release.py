import json

import requests
from flask_restful import Resource, abort

from src.service.resources.service import _get_release_link


class ReleaseResource(Resource):
    @classmethod
    def get(cls):
        try:
            repo_name: str = 'rubix-service'
            resp = requests.get(_get_release_link(repo_name))
            data = json.loads(resp.content)
            releases = []
            for row in data:
                releases.append(row.get('tag_name'))
            return releases
        except Exception as e:
            abort(501, message=str(e))
