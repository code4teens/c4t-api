from database import db_session
from models import Bot, BotSchema
from utils import make_json_response


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
        status = 'Conflict'
        message = f'Bot {id} already exists'

        return make_json_response(status, 409, message)


# GET bots/<id>
def get_one(id):
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is not None:
        data = BotSchema().dump(existing_bot)

        return data
    else:
        status = 'Not Found'
        message = f'Bot {id} not found'

        return make_json_response(status, 404, message)


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
        status = 'Not Found'
        message = f'Bot {id} not found'

        return make_json_response(status, 404, message)


# DELETE bots/<id>
def delete(id):
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is not None:
        db_session.delete(existing_bot)
        db_session.commit()
        status = 'OK'
        message = f'Bot {id} deleted'

        return make_json_response(status, 200, message)
    else:
        status = 'Not Found'
        message = f'Bot {id} not found'

        return make_json_response(status, 404, message)
