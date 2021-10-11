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
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is None:
        bot_schema = BotSchema()
        user = bot_schema.load(bot_data)
        db_session.add(user)
        db_session.commit()
        data = bot_schema.dump(user)

        return data
    else:
        abort(409, f'Bot for ID: {id} already exists')


# GET bots/<id>
def get_one(id):
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is not None:
        bot_schema = BotSchema()
        data = bot_schema.dump(existing_bot)

        return data
    else:
        abort(404, f'Bot not found for ID: {id}')
