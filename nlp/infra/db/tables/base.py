from sqlalchemy import MetaData, Column, Integer


def id_():
    return Column("id", Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)


metadata = MetaData()
