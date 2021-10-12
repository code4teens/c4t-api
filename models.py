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
    password = Column(String(60), nullable=False)
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

    # def __init__(
    #     self, id, password, name, discriminator, display_name, cohort_id,
    #     is_admin=False
    # ):
    #     self.id = id
    #     self.password = bcrypt.hashpw(
    #         password.encode('utf-8'), bcrypt.gensalt()
    #     )
    #     self.name = name
    #     self.discriminator = discriminator
    #     self.display_name = display_name
    #     self.cohort_id = cohort_id
    #     self.is_admin = is_admin


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
    password = fields.String()
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


class BotSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    user_id = fields.Integer()
    msg_id = fields.Integer()
    created_at = fields.DateTime()
    last_updated = fields.DateTime()

    @post_load
    def make_bot(self, data, **kwargs):
        return Bot(**data)


class NestedBotSchema(Schema):
    id = fields.Integer()
