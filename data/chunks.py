import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Chunks(SqlAlchemyBase):
    __tablename__ = 'chunks'

    id = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.TEXT)
