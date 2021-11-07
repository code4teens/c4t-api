import secrets

import bcrypt

from database import db_session
from models import User
from schemata import UserSchema
from utils import admin_only, admin_or_owner_only


# GET users
def get_all():
    users = User.query.order_by(User.id).all()
    data = UserSchema(many=True, exclude=['api_key']).dump(users)

    return data, 200


# POST users
@admin_only
def create(body, **kwargs):
    id = body.get('id')
    name = body.get('name')
    discriminator = body.get('discriminator')
    existing_user_1 = User.query.filter_by(id=id).one_or_none()
    existing_user_2 = User.query.filter_by(name=name)\
        .filter_by(discriminator=discriminator)\
        .one_or_none()

    if existing_user_1 is None and existing_user_2 is None:
        user_schema = UserSchema(exclude=['api_key'])
        user = user_schema.load(body)
        db_session.add(user)
        db_session.commit()
        data = user_schema.dump(user)

        return data, 201
    else:
        data = {
            'title': 'Conflict',
            'status': 409,
            'detail': 'User with posted details already exists'
        }

        return data, 409


# GET users/<id>
def get_one(id):
    user = User.query.filter_by(id=id).one_or_none()

    if user is not None:
        data = UserSchema(exclude=['api_key']).dump(user)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'User {id} not found'
        }

        return data, 404


# PUT users/<id>
@admin_only
def update(id, body, **kwargs):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        user_schema = UserSchema(exclude=['api_key'])
        user = user_schema.load(body)
        user.id = existing_user.id
        db_session.merge(user)
        db_session.commit()
        data = user_schema.dump(existing_user)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'User {id} not found'
        }

        return data, 404


# DELETE users/<id>
@admin_only
def delete(id, **kwargs):
    user = User.query.filter_by(id=id).one_or_none()

    if user is not None:
        db_session.delete(user)
        db_session.commit()
        data = {
            'title': 'OK',
            'status': 200,
            'detail': f'User {id} deleted'
        }

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'User {id} not found'
        }

        return data, 404


# PUT users/<id>/password
@admin_or_owner_only
def update_password(id, body, **kwargs):
    user = User.query.filter_by(id=id).one_or_none()

    if user is not None:
        user.password = bcrypt.hashpw(
            body.get('password').encode('utf-8'), bcrypt.gensalt()
        )
        db_session.merge(user)
        db_session.commit()
        data = {
            'title': 'OK',
            'status': 200,
            'detail': f'Updated password for user {id}'
        }

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'User {id} not found'
        }

        return data, 404


# POST users/<id>/login
def login(id, body):
    user = User.query.filter_by(id=id).one_or_none()

    if user is not None:
        if bcrypt.checkpw(
            body.get('password').encode('utf-8'),
            user.password.encode('utf-8')
        ):
            auth_token = user.encode_auth_token()
            if auth_token:
                data = {
                    'title': 'OK',
                    'status': 200,
                    'detail': f'{auth_token}'
                }

                return data, 200
        else:
            data = {
                'title': 'Unauthorised',
                'status': 401,
                'detail': f'Wrong password for user {id}'
            }

            return data, 401
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'User {id} not found'
        }

        return data, 404


# GET users/<id>/api_key
@admin_or_owner_only
def get_api_key(id, **kwargs):
    user = User.query.filter_by(id=id).one_or_none()

    if user is not None:
        data = UserSchema(only=['api_key']).dump(user)

        return data
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'User {id} not found'
        }

        return data, 404


# PUT users/<id>/api_key
@admin_only
def update_api_key(id, **kwargs):
    user = User.query.filter_by(id=id).one_or_none()

    if user is not None:
        user.api_key = secrets.token_urlsafe(32)
        db_session.merge(user)
        db_session.commit()
        data = {
            'title': 'OK',
            'status': 200,
            'detail': f'Updated API key for user {id}'
        }

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'User {id} not found'
        }

        return data, 404
