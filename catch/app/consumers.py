import json
import random
from datetime import datetime, timedelta
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Challenge, ChallengeDoneByTeam, Team, Game
from .utils import get_next_element_in_cycle

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

            team.coins = team.coins + challenge.reward
            team.save()
            
            ChallengeDoneByTeam.objects.create(challenge = challenge,
                                               team = team,
                                               successful = True,
                                               timestamp = datetime.now())

            self.send(text_data=json.dumps({
                "event": event,
                "send_team": send_team,
                "send_team_coins": team.coins
            }))

        elif event == 'CATCH':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'catch',
                    'event': event,
                    'send_team': send_team
                }
            )

        elif event == 'CATCH-SUCCESS':
            
            current_game = Game.objects.get(game_id = game_id)
            current_team = Team.objects.get(team_name = send_team, game = current_game)
            catched_team = Team.objects.get(game = current_game, role = 'RUNNER')
            all_teams = Team.objects.filter(game = current_game)
            all_teams_pk = Team.objects.filter(game = current_game).values_list("pk", flat=True)
        
            next_team = get_next_element_in_cycle(catched_team.pk, list(all_teams_pk))
            print(next_team)
            Team.objects.filter(pk = catched_team.pk).update(role = 'CHASER')      
            Team.objects.filter(pk = next_team.pk).update(role = 'RUNNER')      
            # catched_team.role = 'CHASER'
            # next_team.role = 'RUNNER'
            # catched_team.save()
            # next_team.save()
            print(next_team.team_name)
            print(next_team.role)
            Team.objects.filter(game_id = current_game, role="CHASER").update(jail_time_start=datetime.now(), jail_time = 5)
                
            print("catch success end")
            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'catch_success',
                    'event': event,
                    'game_id': game_id,
                    'send_team': send_team
                }
            )

        elif event == 'CATCH-DENY':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'catch_deny',
                    'event': event,
                    'send_team': send_team
                }
            )
        

        
    def catch(self, response):
        
        event = response["event"]
        send_team = response["send_team"]
        
        self.send(text_data=json.dumps({
            "send_team": send_team,
            "event": event,
        }))

    def catch_success(self, response):
        
        print("catch success start")
        event = response["event"]
        game_id = response["game_id"]
        send_team = response["send_team"]
    
        

        self.send(text_data=json.dumps({
            "send_team": send_team,
            "game_id": game_id,
            "event": event,
        }))

    def catch_deny(self, response):
    
        event = response["event"]
        send_team = response["send_team"]

        self.send(text_data=json.dumps({
            "send_team": send_team,
            "event": event,
        }))

class WaitingConsumer(WebsocketConsumer):

    def add_team(self, response):
        
        send_team = response["send_team"]
        event = response["event"]
        
        self.send(text_data=json.dumps({
            "send_team": send_team,
            "event": event,
        }))

    def start_game(self, response):
        game_id = response["game_id"]
        event = response["event"]

        self.send(text_data=json.dumps({
            "team_name": game_id,
            "event": event,
        }))

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
        send_team = response.get('send_team', None)
        
        if event == 'START':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'add_team',
                    'send_team': send_team,
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
                    'event': event
                }
            )
        
    
    
