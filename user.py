from flask import abort

from models import User, UserSchema


# users
def get_all():
    user = User.query.order_by(User.id).all()
    user_schema = UserSchema(many=True)
    data = user_schema.dump(user)

    return data


# users/<id>
def get_one(id):
    user = User.query.filter_by(id=id).one_or_none()

    if user is not None:
        user_schema = UserSchema()
        data = user_schema.dump(user)

        return data
    else:
        abort(404, f'User not found for ID: {id}')
