import os

from flask import redirect
import connexion
import jwt

from database import db_session
from utils import make_json_response

basedir = os.path.abspath(os.path.dirname(__file__))
connexion_app = connexion.App(__name__, specification_dir=basedir)
connexion_app.add_api('swagger.yml')


@connexion_app.route('/')
def index():
    return redirect('/api/v1/ui')


@connexion_app.app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()


@connexion_app.app.errorhandler(jwt.exceptions.ExpiredSignatureError)
def expired_jwt(e):
    status = 'Unauthorised'
    message = 'Expired token, please log in again'

    return make_json_response(status, 401, message)


@connexion_app.app.errorhandler(jwt.exceptions.InvalidTokenError)
def invalid_jwt(e):
    status = 'Unauthorised'
    message = 'Invalid token, please log in again'

    return make_json_response(status, 401, message)


if __name__ == '__main__':
    connexion_app.run(host='127.0.0.1', port=8080, debug=True)
