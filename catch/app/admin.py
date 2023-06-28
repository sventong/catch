from django.contrib import admin
from .models import Game, Team

# Register your models here.

class GameAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'created_at', 'updated_at')

admin.site.register(Game, GameAdmin)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'team_name', 'game_master')

admin.site.register(Team, TeamAdmin)
