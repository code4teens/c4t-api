from datetime import datetime, timedelta
import os

from connexion.exceptions import OAuthProblem
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
    xp = Column(Integer, nullable=False, default=0)
    is_admin = Column(Boolean, nullable=False, default=False)
    api_key = Column(String(43), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    bots = relationship(
        'Bot', back_populates='user', order_by='Bot.created_at'
    )
    channels = relationship(
        'Channel', back_populates='user', order_by='Channel.created_at'
    )
    enrolments = relationship(
        'Enrolment', back_populates='user', order_by='Enrolment.id'
    )
    evals_as_evaluator = relationship(
        'Eval',
        foreign_keys='Eval.evaluator_id',
        back_populates='evaluator',
        order_by='Eval.id'
    )
    evals_as_evaluatee = relationship(
        'Eval',
        foreign_keys='Eval.evaluatee_id',
        back_populates='evaluatee',
        order_by='Eval.id'
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

    @staticmethod
    def validate_api_key(api_key, required_scopes):
        user = User.query.filter_by(api_key=api_key).one_or_none()

        if user is None:
            raise OAuthProblem

        payload = {
            'sub': user.id,
            'is_admin': user.is_admin
        }

        return payload


class Bot(Base):
    __tablename__ = 'bot'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=True)
    discriminator = Column(String(4), nullable=True)
    display_name = Column(String(64), nullable=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)
    msg_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    user = relationship('User', back_populates='bots')
    cohort = relationship('Cohort', back_populates='bots')


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=False)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    user = relationship('User', back_populates='channels')
    cohort = relationship('Cohort', back_populates='channels')


class Cohort(Base):
    __tablename__ = 'cohort'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    nickname = Column(String(16), nullable=False)
    duration = Column(SmallInteger, nullable=False)
    start_date = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=True)
    review_schema = Column(JSON, nullable=True)
    feedback_schema = Column(JSON, nullable=True)

    bots = relationship(
        'Bot', back_populates='cohort', order_by='Bot.created_at'
    )
    channels = relationship(
        'Channel', back_populates='cohort', order_by='Channel.created_at'
    )
    enrolments = relationship(
        'Enrolment', back_populates='cohort', order_by='Enrolment.id'
    )
    evals = relationship('Eval', back_populates='cohort', order_by='Eval.id')


class Enrolment(Base):
    __tablename__ = 'enrolment'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)

    user = relationship('User', back_populates='enrolments')
    cohort = relationship('Cohort', back_populates='enrolments')


class Eval(Base):
    __tablename__ = 'eval'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    evaluator_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    evaluatee_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)
    date = Column(Date, nullable=False)
    review = Column(JSON, nullable=True)
    feedback = Column(JSON, nullable=True)

    evaluator = relationship(
        'User',
        foreign_keys=[evaluator_id],
        back_populates='evals_as_evaluator'
    )
    evaluatee = relationship(
        'User',
        foreign_keys=[evaluatee_id],
        back_populates='evals_as_evaluatee'
    )
    cohort = relationship('Cohort', back_populates='evals')
