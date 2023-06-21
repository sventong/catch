from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("game/<str:game_id>", views.game, name="game"),
    path("game", views.game, name="game"),
    path("map", views.MapView.as_view(), name="game"),
]