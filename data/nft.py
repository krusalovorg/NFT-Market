import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class NFT(SqlAlchemyBase):
    __tablename__ = 'nft'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    hash_block = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    rate = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    sale = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    cost = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
