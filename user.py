from models import User, UserSchema


def get_all():
    user = User.query.order_by(User.id).all()
    user_schema = UserSchema(many=True)
    data = user_schema.dump(user)

    return data
