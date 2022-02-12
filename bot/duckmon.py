import random

#test module script
def get_specific_duck():
    duck_id = [0, 1, 2, 3, 4, 5]
    description = ['Feeling dead inside', 'Happy and content', 'Excited']
    attack_coeff = [2, 4, 6 , 8, 10]
    defend_coeff = [1, 2, 3, 4, 5]
    
    return random.choice(duck_id), random.choice(description), random.choice(attack_coeff), random.choice(defend_coeff)


