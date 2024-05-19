import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Request(SqlAlchemyBase):
    __tablename__ = 'faiss'
    text = sqlalchemy.Column(sqlalchemy.TEXT, primary_key=True)
