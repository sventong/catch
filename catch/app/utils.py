import random
import string
from datetime import timedelta
from .models import Game, Team


def random_game_id():
    while True:
        game_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
        if not Game.objects.filter(game_id = game_id).exists():
            return game_id
        
def get_next_element_in_cycle(current_element, all_elements):
    print(all_elements)
    print(current_element)
    current_index = all_elements.index(current_element)
    if current_index == (len(all_elements) - 1):
        next_index = 0
    else:
        next_index = current_index + 1
    
    next_element = Team.objects.get(pk = all_elements[next_index])

    return next_element

def jail_time(current_team):
    if current_team.role == "CHASER":
        jail_time_finish = current_team.jail_time_start + timedelta(hours=2, minutes=5)
        formatted_jail_time = jail_time_finish.strftime("%Y-%m-%dT%H:%M:%S")

        return formatted_jail_time
    else:
        return ""