from flask import abort, jsonify, make_response
import bcrypt

from database import db_session
from models import User, UserSchema


def make_error(status, code, message):
    response_object = {
        'status': status,
        'code': code,
        'message': message
    }

    return make_response(jsonify(response_object)), code


# GET users
def get_all():
    user = User.query.order_by(User.id).all()
    data = UserSchema(many=True, exclude=['password']).dump(user)

    return data


# POST users
def create(body):
    id = body.get('id')
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is None:
        user_schema = UserSchema(exclude=['password'])
        user = user_schema.load(body)
        db_session.add(user)
        db_session.commit()
        data = user_schema.dump(user)

        return data
    else:
        status = 'Conflict'
        message = f'User {id} already exists'

        return make_error(status, 409, message)


# GET users/<id>
def get_one(id):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        data = UserSchema(exclude=['password']).dump(existing_user)

        return data
    else:
        status = 'Not Found'
        message = f'User {id} not found'

        return make_error(status, 404, message)


# PUT users/<id>
def update(id, body):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        user_schema = UserSchema(exclude=['password', 'bots'])
        user = user_schema.load(body)
        user.id = existing_user.id
        db_session.merge(user)
        db_session.commit()
        data = user_schema.dump(existing_user)

        return data
    else:
        status = 'Not Found'
        message = f'User {id} not found'

        return make_error(status, 404, message)


# DELETE users/<id>
def delete(id):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        db_session.delete(existing_user)
        db_session.commit()
        return make_response(f'User for ID: {id} deleted', 200)
    else:
        abort(404, f'User not found for ID: {id}')


# PUT users/<id>/password
def update_password(id, body):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        user = UserSchema().load(body)
        user.id = existing_user.id
        user.password = bcrypt.hashpw(
            body.get('password').encode('utf-8'), bcrypt.gensalt()
        )
        db_session.merge(user)
        db_session.commit()
        response_object = {
            'status': 'OK',
            'code': 200,
            'message': f'Updated password for user {id}'
        }

        return make_response(jsonify(response_object)), 200
    else:
        status = 'Not Found'
        message = f'User {id} not found'

        return make_error(status, 404, message)
