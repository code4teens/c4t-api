from marshmallow import fields, post_load, Schema
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    func,
    String
)

from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    is_admin = fields.Boolean()
    created_at = fields.DateTime()
    last_updated = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
