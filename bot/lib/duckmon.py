import random
import re
from models import DuckType, SpecificDuck
from client import client, session
# import reaction
# test module script


def get_specific_duck(player_id):
    duck_id = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    mood = ['Feeling dead inside', 'Happy and content', 'Excited']
    attack_coeff = [2, 4, 6, 8, 10]
    defend_coeff = [1, 2, 3, 4, 5]
    # switch case for color based on mood
    moodValue = random.choice(mood)
    if moodValue == 'Feeling dead inside':
        colorValue = colorRGB('000000')
    elif moodValue == 'Happy and content':
        colorValue = colorRGB('00FF00')
    elif moodValue == 'Excited':
        colorValue = colorRGB('FA500')

    random_number = random.choice(duck_id)
    duck_types = session.query(DuckType).filter(DuckType.id == random_number).one_or_none()
    duck = SpecificDuck(duck_type=duck_types, nickname="nickname", player_id=player_id)

    return random_number, moodValue, random.choice(attack_coeff), random.choice(defend_coeff), colorValue


def colorRGB(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
