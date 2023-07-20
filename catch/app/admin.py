from django.contrib import admin
from .models import *

# Register your models here.

class GameAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'created_at', 'updated_at')

admin.site.register(Game, GameAdmin)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'team_name', 'game_master')

admin.site.register(Team, TeamAdmin)

class CatchAdmin(admin.ModelAdmin):
    list_display = ('catched_team', 'timestamp')

admin.site.register(Catch, CatchAdmin)

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'challenge_text', 'reward')
    
admin.site.register(Challenge, ChallengeAdmin)

class TransportTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost_per_station')
    
admin.site.register(TransportType, TransportTypeAdmin)

class ChallengeDoneByTeamAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'team', 'successful', 'open', 'timestamp_start', 'timestamp_end')
    
admin.site.register(ChallengeDoneByTeam, ChallengeDoneByTeamAdmin)

class TransportDoneByTeamAdmin(admin.ModelAdmin):
    list_display = ('transport_type', 'team', 'stops', 'timestamp')
    
admin.site.register(TransportDoneByTeam, TransportDoneByTeamAdmin)
