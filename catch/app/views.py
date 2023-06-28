import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView

from .forms import JoinGameForm, CreateGameForm
from .models import Game, Team
from django.conf import settings

GOOGLE_MAPS_API_KEY = settings.GOOGLE_MAPS_API_KEY


# Create your views here.

def index(request):
    
    if request.method == "POST":
        form = JoinGameForm(request.POST)
        if form.is_valid():
            return HttpResponse("Form is Valid... why are we here?")
    else:
        form = JoinGameForm()

    context = {"form": form}
    return render(request, 'home.html', context)

    # return HttpResponse("Hello, world. You're at the polls index.")


# def game_id(request, game_id: str):

#     return HttpResponse(game_id)

def game(request, game_id=""):

    print(game_id)
    game_id = request.GET.get('game_id')

    context = {
        "game_id": game_id
    }
    return render(request, 'game.html', context)

def map(request):
    context = {
        "api_key": GOOGLE_MAPS_API_KEY
    }
    
    return render(request, "map.html", context)


def create_game(request):
    
    form = CreateGameForm
    new_game_id = "testgame" 
    #TODO Generate random Game ID
    #TODO Also change in waiting_for_teams.html

    context = {
        "form": form,
        "new_game_id": new_game_id
    }

    return render(request, "create_game.html", context)

def waiting_for_teams(request):

    if request.method == "POST":
        form = CreateGameForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data['team_name']
            game_id = form.cleaned_data['game_id']
            game_master = form.cleaned_data['game_master']

            game = Game(game_id=game_id)
            game.save()

            team = Team(game_id = game, 
                        team_name = team_name, 
                        game_master = game_master)
            team.save()
    
    elif request.method == "GET":
        print(request.body)
    
    context = {
        "game_id": game_id,
        "team_name": team_name
    }
    return render(request, 'waiting_for_teams.html', context)

def join_game(request):
    if request.method == "POST":
        form = JoinGameForm(request.POST)
        if form.is_valid():
            game_id = form.cleaned_data['game_id']
            game = Game.objects.filter(game_id=game_id)
            if game.exists():
                
                team_name = form.cleaned_data['team_name']
                game_master = form.cleaned_data['game_master']
                team = Team(game_id=game.first(), team_name = team_name, game_master = game_master)
                team.save()
                
                context = {
                    "game_id": game_id,
                    "team_name": team_name
                }
                return render(request, 'waiting_for_teams.html', context)

            else:
                context = {"form": form,
                           "error_message": "GameID does not exist"}

                return render(request, 'home.html', context)