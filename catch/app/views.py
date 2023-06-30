import json
import random
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView

from .forms import JoinGameForm, CreateGameForm
from .models import Game, Team
from .utils import random_game_id
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

    game_id = request.session['current_game']
    print(game_id)

    game = Game.objects.get(game_id = game_id)
    teams = Team.objects.filter(game = game)
    escape_team = random.sample(list(teams), 1)

    print(escape_team)




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
    #TODO Generate random Game ID
    #TODO Also change in waiting_for_teams.html

    context = {
        "form": form,
    }

    return render(request, "create_game.html", context)

def waiting_for_teams(request):

    if request.method == "POST":
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game_id = random_game_id()
            team_name = form.cleaned_data['team_name']

            request.session['current_game'] = game_id
            request.session['current_team'] = team_name
            
            game = Game(game_id = game_id)
            game.save()

            curr_team = Team(game = game, 
                             team_name = team_name, 
                             game_master = True)
            curr_team.save()

            # all_teams = Team.objects.filter(game = game).values_list("team_name", flat=True)
            # all_teams = Team.objects.filter(game_id = Game.objects.get(game_id=game_id)).values_list("team_name", flat=True)

            
    elif request.method == "GET":
        
        game_id = request.session['current_game']
        team_name = request.session['current_team']

    game = Game.objects.get(game_id = game_id)
    curr_team = Team.objects.get(game = game, team_name = team_name)
    all_teams = Team.objects.filter(game = game).values_list("team_name", flat=True)


    context = {
        "game": game,
        "curr_team": curr_team,
        "all_teams": all_teams
    }
    return render(request, 'waiting_for_teams.html', context)

def join_game(request):
    
    if request.method == "POST":
        form = JoinGameForm(request.POST) 
        if form.is_valid():
            game_id = form.cleaned_data['game_id'].upper()
            game = Game.objects.filter(game_id=game_id)
            if game.exists():                
                team_name = form.cleaned_data['team_name']

                request.session['current_game'] = game_id
                request.session['current_team'] = team_name

                team = Team(game = game.first(), team_name = team_name, game_master = False)
                team.save()

                all_teams = Team.objects.filter(game = game.first()).values_list("team_name", flat=True)
                
                context = {
                    "game": game.first(),
                    "curr_team": team,
                    "all_teams": all_teams,
                }
                return render(request, 'waiting_for_teams.html', context)

            else:
                context = {"form": form,
                           "error_message": "GameID does not exist"}

                return render(request, 'home.html', context)

        else:
            return HttpResponse("was da los")
        
    elif request.method == "GET":
        
        game_id = request.session['current_game']
        team_name = request.session['current_team']

        game = Game.objects.get(game_id = game_id)
        curr_team = Team.objects.get(game = game, team_name = team_name)
        all_teams = Team.objects.filter(game = game).values_list("team_name", flat=True)

        context = {
            "game": game,
            "curr_team": curr_team,
            "all_teams": all_teams
        }
        return render(request, 'waiting_for_teams.html', context)