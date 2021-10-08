import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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

engine = create_engine(database_uri)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()
Base.query = db_session.query_property()
