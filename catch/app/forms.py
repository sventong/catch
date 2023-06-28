from django import forms

class JoinGameForm(forms.Form):
    game_id = forms.CharField(label="Game ID", max_length= 10)
    team_name = forms.CharField(label="Team Name", max_length= 16)
    game_master = forms.BooleanField(label="Game Master")

    
class CreateGameForm(forms.Form):
    team_name = forms.CharField(label="Team Name", max_length= 16)
    game_id = forms.CharField(label="Game ID", max_length= 10)
    game_master = forms.BooleanField(label="Game Master")
