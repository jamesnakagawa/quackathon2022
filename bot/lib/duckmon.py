import random
import re
# test module script


def get_specific_duck():
    duck_id = [0, 1, 2, 3, 4, 5]
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

    return random.choice(duck_id), moodValue, random.choice(attack_coeff), random.choice(defend_coeff), colorValue


def colorRGB(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
