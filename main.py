import os

from flask import redirect
import connexion
import jwt

from database import db_session

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
    data = {
        'title': 'Unauthorised',
        'status': 401,
        'detail': 'Expired JWT'
    }

    return data, 401


@connexion_app.app.errorhandler(jwt.exceptions.InvalidTokenError)
def invalid_jwt(e):
    data = {
        'title': 'Unauthorised',
        'status': 401,
        'detail': 'Invalid JWT'
    }

    return data, 401


@connexion_app.app.errorhandler(connexion.exceptions.OAuthProblem)
def invalid_api_key(e):
    data = {
        'title': 'Unauthorised',
        'status': 401,
        'detail': 'Invalid API key'
    }

    return data, 401


if __name__ == '__main__':
    connexion_app.run(host='127.0.0.1', port=8080, debug=True)
