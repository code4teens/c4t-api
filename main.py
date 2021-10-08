import os

import connexion
from flask import redirect

from database import db_session

basedir = os.path.abspath(os.path.dirname(__file__))
connexion_app = connexion.App(__name__, specification_dir=basedir)
connexion_app.add_api('swagger.yml')


@connexion_app.route('/')
def index():
    return redirect('/api/v1/ui')


@connexion_app.app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    connexion_app.run(host='127.0.0.1', port=8080, debug=True)
