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

  def current_battle(self):
    if not 'current_battle_p1' in self and 'current_battle_p2' in self:
      return None
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

  def current_battle(self):
    if not 'current_battle_d1' in self and 'current_battle_d2' in self:
      return None
    return self.current_battle_d1 or self.current_battle_d2

  def attack_stat(self):
    return self.level * self.duck_type.attack_coeff

  def defence_stat(self):
    return self.level * self.duck_type.defend_coeff

  def __repr__(self):
    return "<SpecificDuck(id='%s', nickname='%s')>" % (self.id, self.nickname)

class Battle(Base):
  __tablename__ = 'battle'

  id = Column(Integer, primary_key=True)
  player1_id = Column(ForeignKey('player.id'))
  player2_id = Column(ForeignKey('player.id'))
  player1 = relationship("Player", back_populates="current_battle_p1", foreign_keys=[player1_id])
  player2 = relationship("Player", back_populates="current_battle_p2", foreign_keys=[player2_id])
  duck1_id = Column(ForeignKey('specific_duck.id'))
  duck2_id = Column(ForeignKey('specific_duck.id'), nullable=True)
  duck1 = relationship("SpecificDuck", back_populates="current_battle_d1", foreign_keys=[duck1_id])
  duck2 = relationship("SpecificDuck", back_populates="current_battle_d2", foreign_keys=[duck2_id])
  accepted = Column(Boolean, default=False)
  turn: Column(Integer, default=0)
  completed = Column(Boolean, default=False)

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

Player.current_battle_p1 = relationship("Battle", back_populates="player1", foreign_keys=[Battle.player1_id])
Player.current_battle_p2 = relationship("Battle", back_populates="player2", foreign_keys=[Battle.player2_id])
SpecificDuck.current_battle_d1 = relationship("Battle", back_populates="duck1", foreign_keys=[Battle.duck1_id])
SpecificDuck.current_battle_d2 = relationship("Battle", back_populates="duck2", foreign_keys=[Battle.duck2_id])

class GameState(Base):
  __tablename__ = 'state'

  id = Column(Integer, primary_key=True)
  wild_duck = relationship("SpecificDuck")
  wild_duck_id = Column(ForeignKey('specific_duck.id'))

Base.metadata.create_all(engine)
Session = sessionmaker(engine)
