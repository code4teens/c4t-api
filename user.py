import bcrypt

from database import db_session
from models import User, UserSchema
from utils import admin_only, admin_or_owner_only, make_json_response


# GET users
def get_all():
    users = User.query.order_by(User.id).all()
    data = UserSchema(many=True, exclude=['password']).dump(users)

    return data


# POST users
@admin_only
def create(body, **kwargs):
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
        title = 'Conflict'
        detail = f'User {id} already exists'

        return make_json_response(title, 409, detail)


# GET users/<id>
def get_one(id):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        data = UserSchema(exclude=['password']).dump(existing_user)

        return data
    else:
        title = 'Not Found'
        detail = f'User {id} not found'

        return make_json_response(title, 404, detail)


# PUT users/<id>
@admin_only
def update(id, body, **kwargs):
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
        title = 'Not Found'
        detail = f'User {id} not found'

        return make_json_response(title, 404, detail)


# DELETE users/<id>
@admin_only
def delete(id, **kwargs):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        db_session.delete(existing_user)
        db_session.commit()
        title = 'OK'
        detail = f'User {id} deleted'

        return make_json_response(title, 200, detail)
    else:
        title = 'Not Found'
        detail = f'User {id} not found'

        return make_json_response(title, 404, detail)


# PUT users/<id>/password
@admin_or_owner_only
def update_password(id, body, **kwargs):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        user = UserSchema().load(body)
        user.id = existing_user.id
        user.password = bcrypt.hashpw(
            body.get('password').encode('utf-8'), bcrypt.gensalt()
        )
        db_session.merge(user)
        db_session.commit()
        title = 'OK'
        detail = f'Updated password for user {id}'

        return make_json_response(title, 200, detail)
    else:
        title = 'Not Found'
        detail = f'User {id} not found'

        return make_json_response(title, 404, detail)


# POST users/<id>/login
def login(id, body):
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is not None:
        if bcrypt.checkpw(
            body.get('password').encode('utf-8'),
            existing_user.password.encode('utf-8')
        ):
            auth_token = existing_user.encode_auth_token()
            if auth_token:
                title = 'OK'
                detail = f'{auth_token}'

                return make_json_response(title, 200, detail)
        else:
            title = 'Unauthorised'
            detail = f'Wrong password for user {id}'

            return make_json_response(title, 401, detail)
    else:
        title = 'Not Found'
        detail = f'User {id} not found'

        return make_json_response(title, 404, detail)
