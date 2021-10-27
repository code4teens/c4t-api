from database import db_session
from models import Bot, BotSchema
from utils import admin_only, make_json_response


# GET bots
def get_all():
    bots = Bot.query.order_by(Bot.id).all()
    data = BotSchema(many=True).dump(bots)

    return data


# POST bots
@admin_only
def create(body, **kwargs):
    id = body.get('id')
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is None:
        bot_schema = BotSchema()
        bot = bot_schema.load(body)
        db_session.add(bot)
        db_session.commit()
        data = bot_schema.dump(bot)

        return data, 201
    else:
        title = 'Conflict'
        detail = f'Bot {id} already exists'

        return make_json_response(title, 409, detail)


# GET bots/<id>
def get_one(id):
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is not None:
        data = BotSchema().dump(existing_bot)

        return data
    else:
        title = 'Not Found'
        detail = f'Bot {id} not found'

        return make_json_response(title, 404, detail)


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

        return data
    else:
        title = 'Not Found'
        detail = f'Bot {id} not found'

        return make_json_response(title, 404, detail)


# DELETE bots/<id>
@admin_only
def delete(id, **kwargs):
    existing_bot = Bot.query.filter_by(id=id).one_or_none()

    if existing_bot is not None:
        db_session.delete(existing_bot)
        db_session.commit()
        title = 'OK'
        detail = f'Bot {id} deleted'

        return make_json_response(title, 200, detail)
    else:
        title = 'Not Found'
        detail = f'Bot {id} not found'

        return make_json_response(title, 404, detail)
