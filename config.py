import os

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
connection = os.environ.get('MYSQL_CONNECTION')
username = os.environ.get('MYSQL_USERNAME')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('MYSQL_DATABASE')

if connection is not None:
    database_uri = (
        f'mysql+pymysql://{username}:{password}@localhost/{database}'
        f'?unix_socket=/cloudsql/{connection}'
    )
else:
    database_uri = (
        f'mysql+pymysql://{username}:{password}@127.0.0.1:3306/{database}'
    )

connexion_app = connexion.App(__name__, specification_dir=basedir)
app = connexion_app.app
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
