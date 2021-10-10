from flask import abort

from database import db_session
from models import Bot, BotSchema


# GET bots
def get_all():
    bot = Bot.query.order_by(Bot.id).all()
    bot_schema = BotSchema(many=True)
    data = bot_schema.dump(bot)

    return data


# POST bots
def create(bot_data):
    id = bot_data.get('id')
    existing_user = Bot.query.filter_by(id=id).one_or_none()

    if existing_user is None:
        bot_schema = BotSchema()
        user = bot_schema.load(bot_data)
        db_session.add(user)
        db_session.commit()
        data = bot_schema.dump(user)

        return data
    else:
        abort(409, f'Bot for ID: {id} already exists')
