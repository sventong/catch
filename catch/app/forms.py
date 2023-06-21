from django import forms

class JoinGameForm(forms.Form):
    game_id = forms.CharField(label="Game ID", max_length= 10)

    
