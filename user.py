import bcrypt

from database import db_session
from models import User, UserSchema
from utils import make_json_response


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
        user_schema = UserSchema(exclude=['password', 'bots'])
        user = user_schema.load(body)
        db_session.add(user)
        db_session.commit()
        data = user_schema.dump(user)

        return data, 201
    else:
        status = 'Conflict'
        message = f'User {id} already exists'

        return make_json_response(status, 409, message)


# GET users/<id>
def get_one(id):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        data = UserSchema(exclude=['password']).dump(existing_user)

        return data
    else:
        status = 'Not Found'
        message = f'User {id} not found'

        return make_json_response(status, 404, message)


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

        return make_json_response(status, 404, message)


# DELETE users/<id>
def delete(id):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        db_session.delete(existing_user)
        db_session.commit()
        status = 'OK'
        message = f'User {id} deleted'

        return make_json_response(status, 200, message)
    else:
        status = 'Not Found'
        message = f'User {id} not found'

        return make_json_response(status, 404, message)


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
        status = 'OK'
        message = f'Updated password for user {id}'

        return make_json_response(status, 200, message)
    else:
        status = 'Not Found'
        message = f'User {id} not found'

        return make_json_response(status, 404, message)
