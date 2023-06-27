from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("game/<str:game_id>", views.game, name="game"),
    path("game", views.game, name="game"),
    path("map", views.map, name="map"),
    path("create_game/", views.create_game, name="create_game"),
    path("waiting_for_teams/", views.waiting_for_teams, name="waiting_for_teams")
]