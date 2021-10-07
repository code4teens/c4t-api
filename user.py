from flask import abort

from config import db
from models import User, UserSchema


# GET users
def get_all():
    user = User.query.order_by(User.id).all()
    user_schema = UserSchema(many=True)
    data = user_schema.dump(user)

    return data


# POST users
def create(user):
    id = user.get('id')
    existing_user = User.query.filter_by(id=id).one_or_none()

    if existing_user is None:
        user_schema = UserSchema()
        new_user = user_schema.load(user, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        data = user_schema.dump(new_user)

        return data
    else:
        abort(409, f'User for ID: {id} already exists.')


# GET users/<id>
def get_one(id):
    user = User.query.filter_by(id=id).one_or_none()

    if user is not None:
        user_schema = UserSchema()
        data = user_schema.dump(user)

        return data
    else:
        abort(404, f'User not found for ID: {id}')
