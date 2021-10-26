import os

from flask import redirect
import connexion
import jwt

from database import db_session
from utils import make_json_response

basedir = os.path.abspath(os.path.dirname(__file__))
connexion_app = connexion.App(__name__, specification_dir=basedir)
connexion_app.add_api('swagger.yaml')


@connexion_app.route('/')
def index():
    return redirect('/api/v1/ui')


@connexion_app.app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()


@connexion_app.app.errorhandler(jwt.exceptions.ExpiredSignatureError)
def expired_jwt(e):
    title = 'Unauthorised'
    detail = 'Expired token'

    return make_json_response(title, 401, detail)


@connexion_app.app.errorhandler(jwt.exceptions.InvalidTokenError)
def invalid_jwt(e):
    title = 'Unauthorised'
    detail = 'Invalid token'

    return make_json_response(title, 401, detail)


if __name__ == '__main__':
    connexion_app.run(host='127.0.0.1', port=8080, debug=True)
