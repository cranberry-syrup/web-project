import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Job(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    salary = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_public = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    