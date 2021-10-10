from marshmallow import fields, post_load, Schema
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    func,
    SmallInteger,
    String
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)
    cohort_id = Column(SmallInteger, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    bots = relationship('Bot', back_populates='user', order_by='Bot.id')


class Bot(Base):
    __tablename__ = 'bot'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    msg_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    user = relationship('User', back_populates='bots')


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    cohort_id = fields.Integer()
    is_admin = fields.Boolean()
    created_at = fields.DateTime()
    last_updated = fields.DateTime()

    bots = fields.Nested('NestedBotSchema', default=[], many=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class NestedBotSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    msg_id = fields.Integer()
    created_at = fields.DateTime()
    last_updated = fields.DateTime()


class BotSchema(NestedBotSchema):
    user_id = fields.Integer()
