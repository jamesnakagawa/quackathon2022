from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, String, Column, Text, DateTime, ForeignKey, Integer, Float
from datetime import datetime

engine = create_engine('sqlite:///sqlite3.db') # using relative path
engine.connect()

metadata = MetaData()

player = Table('player', metadata,
    Column('id', Integer(), primary_key=True),
    Column('handle', String(64), nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

duck_type = Table('duck_type', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(64), nullable=False),
    Column('description', Text(),  nullable=True),
    Column('attack_coeff', Float(), nullable=False),
    Column('defend_coeff', Float(), nullable=False),
    Column('hp_coeff', Float(), nullable=False),
    Column('image_url', String(256), nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

specific_duck = Table('specific_duck', metadata,
    Column('id', Integer(), primary_key=True),
    Column('duck_type_id', ForeignKey('duck_type.id')),
    Column('player_id', ForeignKey('player.id')),
    Column('nickname', String(64), nullable=False),
    Column('level', Integer(), nullable=False),
    Column('current_hp', Integer(), nullable=False),
    Column('current_xp', Integer(), nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)
