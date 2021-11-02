from database import db_session
from models import Channel, ChannelSchema
from utils import admin_only, make_json_response


# GET channels
def get_all():
    channels = Channel.query.order_by(Channel.id).all()
    data = ChannelSchema(many=True).dump(channels)

    return data


# POST channels
@admin_only
def create(body, **kwargs):
    id = body.get('id')
    existing_channel = Channel.query.filter_by(id=id).one_or_none()

    if existing_channel is None:
        channel_schema = ChannelSchema()
        channel = channel_schema.load(body)
        db_session.add(channel)
        db_session.commit()
        data = channel_schema.dump(channel)

        return data, 201
    else:
        title = 'Conflict'
        detail = f'Channel {id} already exists'

        return make_json_response(title, 409, detail)


# GET channels/<id>
def get_one(id):
    channel = Channel.query.filter_by(id=id).one_or_none()

    if channel is not None:
        data = ChannelSchema().dump(channel)

        return data
    else:
        title = 'Not Found'
        detail = f'Channel {id} not found'

        return make_json_response(title, 404, detail)


# PUT channels/<id>
@admin_only
def update(id, body, **kwargs):
    existing_channel = Channel.query.filter_by(id=id).one_or_none()

    if existing_channel is not None:
        channel_schema = ChannelSchema()
        channel = channel_schema.load(body)
        channel.id = existing_channel.id
        db_session.merge(channel)
        db_session.commit()
        data = channel_schema.dump(existing_channel)

        return data
    else:
        title = 'Not Found'
        detail = f'Channel {id} not found'

        return make_json_response(title, 404, detail)


# DELETE channels/<id>
@admin_only
def delete(id, **kwargs):
    channel = Channel.query.filter_by(id=id).one_or_none()

    if channel is not None:
        db_session.delete(channel)
        db_session.commit()
        title = 'OK'
        detail = f'Channel {id} deleted'

        return make_json_response(title, 200, detail)
    else:
        title = 'Not Found'
        detail = f'Channel {id} not found'

        return make_json_response(title, 404, detail)
