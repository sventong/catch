import random
import string
from .models import Game



def random_game_id():
    while True:
        game_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
        if not Game.objects.filter(game_id = game_id).exists():
            return game_id