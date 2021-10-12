from flask import abort, make_response

from database import db_session
from models import Bot, BotSchema


# GET bots
def get_all():
    bot = Bot.query.order_by(Bot.id).all()
    data = BotSchema(many=True).dump(bot)

    return data


# POST bots
def create(body):
    id = body.get('id')
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is None:
        bot_schema = BotSchema()
        user = bot_schema.load(body)
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


# PUT bots/<id>
def update(id, body):
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is not None:
        bot_schema = BotSchema()
        bot = bot_schema.load(body)
        bot.id = existing_bot.id
        db_session.merge(bot)
        db_session.commit()
        data = bot_schema.dump(existing_bot)

        return data
    else:
        abort(404, f'Bot not found for ID: {id}')


# DELETE bots/<id>
def delete(id):
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is not None:
        db_session.delete(existing_bot)
        db_session.commit()
        return make_response(f'Bot for ID: {id} deleted', 200)
    else:
        abort(404, f'Bot not found for ID: {id}')
