from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import String, Column, Text, DateTime, ForeignKey, Integer, Float, Boolean
from datetime import datetime
from random import randint

engine = create_engine('sqlite:///sqlite3.db') # using relative path
engine.connect()

Base = declarative_base()

class Player(Base):
  __tablename__ = 'player'

  id = Column(Integer, primary_key=True)
  handle = Column(String, nullable=False)
  created_on = Column(DateTime, default=datetime.now)
  updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
  ducks = relationship("SpecificDuck", back_populates="player")
  current_battle_p1 = relationship("Battle", back_populates="player1")
  current_battle_p2 = relationship("Battle", back_populates="player2")

  def current_battle(self):
    return self.current_battle_p1 or self.current_battle_p2

  def available_ducks(self):
    return [duck for duck in self.ducks if duck.fainted_on is None]

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
  current_battle_d1 = relationship("Battle", back_populates="duck1")
  current_battle_d2 = relationship("Battle", back_populates="duck2")

  def current_battle(self):
    return self.current_battle_d1 or self.current_battle_d2

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
  level = Column(Integer, nullable=False, default=1)
  current_hp = Column(Integer, nullable=False, default=100)
  current_xp = Column(Integer, nullable=False, default=0)
  fainted_on = Column(DateTime, nullable=True)
  created_on = Column(DateTime, default=datetime.now)
  updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  def attack_stat(self):
    return self.level * self.duck_type.attack_coeff

  def defence_stat(self):
    return self.level * self.duck_type.defend_coeff

  def __repr__(self):
    return "<SpecificDuck(id='%s', nickname='%s')>" % (self.id, self.nickname)

class Battle(Base):
  id: Column(Integer, primary_key=True)
  player1_id = Column(ForeignKey('player1.id'))
  player2_id = Column(ForeignKey('player2.id'))
  player1 = relationship("Player", back_populates="current_battle")
  player2 = relationship("Player", back_populates="current_battle")
  duck1_id = Column(ForeignKey('duck1.id'))
  duck2_id = Column(ForeignKey('duck2.id'), nullable=True)
  duck1 = relationship("Duck", back_populates="current_battle")
  duck2 = relationship("Duck", back_populates="current_battle")
  accepted: Column(Boolean, default=False)
  turn: Column(Integer, default=0)
  completed: Column(Boolean, default=False)

  def accept(self, duck):
    self.duck2 = duck
    self.accepted = True

  def attacker(self):
    if (self.turn % 2 == 0):
      return self.duck1
    return self.duck2

  def defender(self):
    if (self.turn % 2 == 0):
      return self.duck2
    return self.duck1

  def do_turn(self, choice):
    if (choice == 1):
      attacker_duck = self.attacker
      defender_duck = self.defender
      attack = randint(8, 12) * attacker_duck.attack / defender_duck.defence
      if (defender_duck.current_hp < attack):
        defender_duck.fainted_on = datetime.now
        return False
      else:
        defender_duck.current_hp -= attack
        self.turn += 1
        return True

class GameState(Base):
  id: Column(Integer, primary_key=True)
  wild_duck = relationship("Duck")
  wild_duck_id: Column(ForeignKey('wild_duck.id'))

Base.metadata.create_all(engine)
Session = sessionmaker(engine)
