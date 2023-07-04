import json
import random
from datetime import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Challenge, ChallengeDoneByTeam, Team, Game

class GameConsumer(WebsocketConsumer):

    def connect(self):
        print("Connect")
        #print("self.scope")
        self.room_group_name = self.scope['url_route']['kwargs']['game_id']
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        print("Disconnected")
        # Join room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        response = json.loads(text_data)
        
        event = response.get("event", None)
        send_team = response.get('send_team', None)
        game_id = response.get('game_id', None)
        
        if event == 'GET-CHALLENGE':
            
            all_challenges = Challenge.objects.all()
            random_challenge = random.choice(list(all_challenges))

            self.send(text_data=json.dumps({
                "event": event,
                "send_team": send_team,
                "challenge_pk": random_challenge.pk,
                "challenge_name": random_challenge.name,
                "challenge_text": random_challenge.challenge_text,
                "challenge_reward": random_challenge.reward,
            }))
        
        elif event == 'CHALLENGE-SUCCESSFUL':
            challenge_pk = response.get("challenge_pk", None)
            challenge = Challenge.objects.get(pk=challenge_pk)
            game = Game.objects.get(game_id = game_id)
            team = Team.objects.get(game = game, team_name = send_team)
            print(team)
            team.coins = team.coins + challenge.reward
            team.save()
            
            ChallengeDoneByTeam.objects.create(challenge = challenge,
                                               team = team,
                                               successful = True,
                                               timestamp = datetime.now())

            self.send(text_data=json.dumps({
                "event": event,
                "send_team": send_team,
            }))
        
 
        

    def start_game(self, response):
        game_id = response["game_id"]
        event = response["event"]

        self.send(text_data=json.dumps({
            "team_name": game_id,
            "event": event,
        }))

class WaitingConsumer(WebsocketConsumer):

    def connect(self):
        print("Connect")
        #print("self.scope")
        self.room_group_name = self.scope['url_route']['kwargs']['game_id']
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        print("Disconnected")
        print(code)
        # Join room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        response = json.loads(text_data)
        event = response.get("event", None)
        team_name = response.get('team_name', None)
        
        if event == 'START':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'add_team',
                    'team_name': team_name,
                    'event': 'NEWTEAM'
                }
            )
        
        elif event == 'START-GAME':
            game_id = response.get('game_id', None)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'start_game',
                    'game_id': game_id,
                    'event': 'START-GAME'
                }
            )
        
    
    def add_team(self, response):
        
        team_name = response["team_name"]
        event = response["event"]
        
        self.send(text_data=json.dumps({
            "team_name": team_name,
            "event": event,
        }))

    def start_game(self, response):
        game_id = response["game_id"]
        event = response["event"]

        self.send(text_data=json.dumps({
            "team_name": game_id,
            "event": event,
        }))
