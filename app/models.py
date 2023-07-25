import uuid
import random
import string

from django.db import models

# Create your models here.


class Game(models.Model):
    game_id = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.game_id}"

RUN = "RUNNER"
CHA = "CHASER"

ROLE_CHOICES = {
    (RUN, "Runner"),
    (CHA, "Chaser")
}
class Team(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=30)
    game_master = models.BooleanField()
    role = models.CharField(max_length=20, choices = ROLE_CHOICES, null=True)
    points = models.IntegerField(null=True, default=0)
    coins = models.IntegerField(null=True, default=500)
    jail_time = models.IntegerField(null=True, blank=True)
    jail_time_start = models.DateTimeField(null=True, blank=True)

    # TODO Solo or Team

class Catch(models.Model):
    catched_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

class Challenge(models.Model):
    name = models.CharField(max_length=255)
    challenge_text = models.TextField()
    reward = models.IntegerField()

class TransportType(models.Model):
    name = models.CharField(max_length=20)
    javascript_id = models.CharField(max_length=20, default="")
    cost_per_station = models.IntegerField()

class ChallengeDoneByTeam(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    successful = models.BooleanField(default=False)
    open = models.BooleanField(default=True)
    timestamp_start = models.DateTimeField(null=True, blank=True)
    timestamp_end = models.DateTimeField(null=True, blank=True)
    

class TransportDoneByTeam(models.Model):
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    stops = models.IntegerField()
    timestamp = models.DateTimeField()




# ROLE_CHOICES = {
#     ('U1', "U1"),
#     ('U2', "U2"),
#     ('U3', "U3"),
#     ('U4', "U4"),
#     ('U5', "U5"),
#     ('U6', "U6")
# }
# class UbahnStation(models.Model):
#     name = models.CharField(max_length=20)
#     line = 
