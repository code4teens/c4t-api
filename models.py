from datetime import datetime, timedelta
import os

from marshmallow import fields, post_load, Schema
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    func,
    Integer,
    JSON,
    SmallInteger,
    String
)
from sqlalchemy.orm import relationship
import jwt

from database import Base
from utils import tz


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    password = Column(String(60), nullable=False)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)
    xp = Column(Integer, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    bots = relationship(
        'Bot', back_populates='user', order_by='Bot.created_at'
    )
    enrolments = relationship(
        'Enrolment', back_populates='user', order_by='Enrolment.id'
    )

    def encode_auth_token(self):
        try:
            payload = {
                'exp': datetime.now(tz) + timedelta(seconds=1200),
                'iat': datetime.now(tz),
                'sub': self.id,
                'is_admin': self.is_admin
            }

            return jwt.encode(
                payload,
                os.environ.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        return jwt.decode(
            auth_token, os.environ.get('SECRET_KEY'), algorithms=['HS256']
        )


class Bot(Base):
    __tablename__ = 'bot'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    msg_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    user = relationship('User', back_populates='bots')


class Cohort(Base):
    __tablename__ = 'cohort'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    nickname = Column(String(16), nullable=False)
    duration = Column(SmallInteger, nullable=False)
    start_date = Column(Date, nullable=False)
    review_schema = Column(JSON, nullable=True)
    feedback_schema = Column(JSON, nullable=True)

    enrolments = relationship(
        'Enrolment', back_populates='cohort', order_by='Enrolment.id'
    )


class Enrolment(Base):
    __tablename__ = 'enrolment'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)

    user = relationship('User', back_populates='enrolments')
    cohort = relationship('Cohort', back_populates='enrolments')


class UserSchema(Schema):
    id = fields.Integer()
    password = fields.String()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    xp = fields.Integer()
    is_admin = fields.Boolean()
    created_at = fields.DateTime()
    last_updated = fields.DateTime()

    bots = fields.Nested('NestedBotSchema', default=[], many=True)
    enrolments = fields.Nested(
        'NestedUserEnrolmentSchema', default=[], many=True
    )

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class NestedUserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()


class BotSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    msg_id = fields.Integer()
    created_at = fields.DateTime()
    last_updated = fields.DateTime()

    user = fields.Nested('NestedUserSchema')

    @post_load
    def make_bot(self, data, **kwargs):
        return Bot(**data)


class NestedBotSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()


class CohortSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    nickname = fields.String()
    duration = fields.Integer()
    start_date = fields.Date()
    review_schema = fields.Dict(allow_none=True)
    feedback_schema = fields.Dict(allow_none=True)

    enrolments = fields.Nested(
        'NestedCohortEnrolmentSchema', default=[], many=True
    )

    @post_load
    def make_cohort(self, data, **kwargs):
        return Cohort(**data)


class NestedCohortSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    nickname = fields.String()


class EnrolmentSchema(Schema):
    id = fields.Integer()

    users = fields.Nested('NestedUserSchema', default=[], many=True)
    cohort = fields.Nested('NestedCohortSchema')


class NestedUserEnrolmentSchema(Schema):
    id = fields.Integer()

    cohort = fields.Nested('NestedCohortSchema')


class NestedCohortEnrolmentSchema(Schema):
    id = fields.Integer()

    user = fields.Nested('NestedUserSchema')
