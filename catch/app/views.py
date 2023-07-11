import json
import random
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.conf import settings

from .forms import JoinGameForm, CreateGameForm
from .models import Game, Team, TransportType, ROLE_CHOICES
from .utils import random_game_id, get_next_element_in_cycle, jail_time

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

    # nr_of_teams = teams.count()
    

    
    

def game(request, game_id=""):

    current_game = Game.objects.get(game_id = request.session['current_game'])
    current_team = Team.objects.get(team_name = request.session['current_team'], game = current_game)
    # catched_team = Team.objects.get(game = current_game, role = 'RUNNER')
    all_teams = Team.objects.filter(game = current_game)
    all_teams_pk = Team.objects.filter(game = current_game).values_list("pk", flat=True)

    state = request.session['state']
    formatted_jail_time = ""
    
    print(state)
    if state == 'waiting':
        if current_team.game_master == True:

            Team.objects.filter(game_id = current_game).update(role="CHASER")
            random_team = random.choice(list(all_teams))
            Team.objects.filter(pk = random_team.pk).update(role="RUNNER")
            Team.objects.filter(game_id = current_game, role="CHASER").update(jail_time_start=datetime.now(), jail_time = 10)
            
            request.session['state'] = 'init_game'
            print(Team.objects.filter(game = current_game, role="RUNNER").first())
        request.session['state'] = 'init_game'

    elif state == 'init_game':
        formatted_jail_time = jail_time(current_team)
        request.session['state'] = 'game'

    elif state == 'game':
        print('Game')
        
    # runner_team = Team.objects.filter(pk=runner_team_pk)
    

    runner_team = Team.objects.filter(game = current_game, role="RUNNER").first()

    context = {
        "game": current_game,
        "curr_team": current_team,
        "all_teams": all_teams,
        "jail_time_finish": formatted_jail_time,
        "transport_types": TransportType.objects.all()
    }

    request.session['current_game'] = game_id
    request.session['current_team'] = current_team.team_name
    
    print(current_team.team_name)
    print(current_team.role)
    print(runner_team.team_name)
    print(runner_team.role)
    
    if current_team == runner_team:
        return render(request, 'game_runner.html', context)
    else:
        return render(request, 'game_chaser.html', context)




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
            request.session['state'] = 'waiting'
            
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
                request.session['state'] = 'waiting'

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
    
