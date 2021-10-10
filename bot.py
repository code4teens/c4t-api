from database import db_session
from models import Bot, BotSchema


# GET bots
def get_all():
    bot = Bot.query.order_by(Bot.id).all()
    bot_schema = BotSchema(many=True)
    data = bot_schema.dump(bot)

    return data
