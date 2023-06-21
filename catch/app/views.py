import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView

from .forms import JoinGameForm


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

class MapView(TemplateView):
    template_name = "map.html"


