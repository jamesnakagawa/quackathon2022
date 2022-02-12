from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import MetaData, String, Column, Text, DateTime, ForeignKey, Integer, Float
from datetime import datetime

engine = create_engine('sqlite:///sqlite3.db') # using relative path
engine.connect()

Base = declarative_base()
metadata = MetaData()

class Player(Base):
  __tablename__ = 'player'

  id = Column(Integer, primary_key=True)
  handle = Column(String, nullable=False)
  created_on = Column(DateTime, default=datetime.now)
  updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
  ducks = relationship("SpecificDuck", back_populates="player")

  def __repr__(self):
    return "<Player(id='%s', handle='%s')>" % (self.id, self.handle)

class DuckType(Base):
  __tablename__ = 'duck_type'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  description = Column(Text,  nullable=True)
  attack_coeff = Column(Float, nullable=False)
  defend_coeff = Column(Float, nullable=False)
  hp_coeff = Column(Float, nullable=False)
  image_url = Column(String, nullable=False)
  created_on = Column(DateTime, default=datetime.now)
  updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
  specific_ducks = relationship("SpecificDuck", back_populates="duck_type")

  def __repr__(self):
    return "<DuckType(id='%s', name='%s')>" % (self.id, self.name)

class SpecificDuck(Base):
  __tablename__ = 'specific_duck'

  id = Column(Integer, primary_key=True)
  duck_type_id = Column(ForeignKey('duck_type.id'))
  duck_type = relationship("DuckType", back_populates="specific_ducks")
  player_id = Column(ForeignKey('player.id'))
  player = relationship("Player", back_populates="ducks")
  nickname = Column(String, nullable=False)
  level = Column(Integer, nullable=False)
  current_hp = Column(Integer, nullable=False)
  current_xp = Column(Integer, nullable=False)
  created_on = Column(DateTime, default=datetime.now)
  updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  def __repr__(self):
    return "<SpecificDuck(id='%s', nickname='%s')>" % (self.id, self.nickname)

Base.metadata.create_all(engine)
Session = sessionmaker(engine)
