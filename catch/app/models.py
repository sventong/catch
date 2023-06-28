from django.db import models

# Create your models here.

class Game(models.Model):
    game_id = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.game_id}"

class Team(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=30)
    game_master = models.BooleanField()
    # TODO Solo or Team