from database import db_session
from models import Bot
from schemata import BotSchema
from utils import admin_only


# GET bots
def get_all():
    bots = Bot.query.order_by(Bot.id).all()
    data = BotSchema(many=True).dump(bots)

    return data, 200


# POST bots
@admin_only
def create(body, **kwargs):
    id = body.get('id')
    name = body.get('name')
    discriminator = body.get('discriminator')
    existing_bot_1 = Bot.query.filter_by(id=id).one_or_none()
    existing_bot_2 = Bot.query.filter_by(name=name)\
        .filter_by(discriminator=discriminator)\
        .one_or_none()

    if existing_bot_1 is None and existing_bot_2 is None:
        bot_schema = BotSchema()
        bot = bot_schema.load(body)
        db_session.add(bot)
        db_session.commit()
        data = bot_schema.dump(bot)

        return data, 201
    else:
        data = {
            'title': 'Conflict',
            'status': 409,
            'detail': 'Bot with posted details already exists'
        }

        return data, 409


# GET bots/<id>
def get_one(id):
    bot = Bot.query.filter_by(id=id).one_or_none()

    if bot is not None:
        data = BotSchema().dump(bot)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Bot {id} not found'
        }

        return data, 404


# PUT bots/<id>
@admin_only
def update(id, body, **kwargs):
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is not None:
        bot_schema = BotSchema()
        bot = bot_schema.load(body)
        bot.id = existing_bot.id
        db_session.merge(bot)
        db_session.commit()
        data = bot_schema.dump(existing_bot)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Bot {id} not found'
        }

        return data, 404


# DELETE bots/<id>
@admin_only
def delete(id, **kwargs):
    bot = Bot.query.filter_by(id=id).one_or_none()

    if bot is not None:
        db_session.delete(bot)
        db_session.commit()
        data = {
            'title': 'OK',
            'status': 200,
            'detail': f'Bot {id} deleted'
        }

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Bot {id} not found'
        }

        return data, 404
