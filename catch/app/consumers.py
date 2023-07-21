import json
import random
from datetime import datetime, timedelta
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Challenge, ChallengeDoneByTeam, Team, Game, TransportType, TransportDoneByTeam, Catch
from .utils import get_next_element_in_cycle, jail_time_end

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
            game = Game.objects.get(game_id = game_id)
            team = Team.objects.get(game = game, team_name = send_team)

            cdbt = ChallengeDoneByTeam.objects.filter(team = team).values_list("challenge__pk", flat=True).distinct()
            print(cdbt)
            all_avail_challenges = Challenge.objects.filter().exclude(pk__in=cdbt)
            print(all_avail_challenges)
            random_challenge = random.choice(list(all_avail_challenges))

            ChallengeDoneByTeam.objects.create(challenge = random_challenge,
                                               team = team,
                                               successful = False,
                                               open = True,
                                               timestamp_start = datetime.now())

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
            team.points += 1
            team.save()

            ChallengeDoneByTeam.objects.filter(challenge = challenge, team = team).update(successful=True, open=False, timestamp_end=datetime.now())
            
            self.send(text_data=json.dumps({
                "event": event,
                "send_team": send_team,
                "send_team_coins": team.coins
            }))

        elif event == 'CHALLENGE-CANCEL':
            challenge_pk = response.get("challenge_pk")
            print(challenge_pk)
            challenge = Challenge.objects.get(pk=challenge_pk)
            game = Game.objects.get(game_id = game_id)
            Team.objects.filter(game = game, team_name = send_team).update(jail_time_start=datetime.now(), jail_time = 1)
            team = Team.objects.get(game = game, team_name = send_team)
            formatted_jail_time = jail_time_end(team.pk)

            ChallengeDoneByTeam.objects.filter(challenge=challenge, team=team).update(successful=False, open=False, timestamp_end=datetime.now())

            self.send(text_data=json.dumps({
                "event": event,
                "send_team": send_team,
                "jail_time_finish": formatted_jail_time,
                "challenge_pk": challenge_pk
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
            
            Team.objects.filter(pk = catched_team.pk).update(role = 'CHASER')      
            Team.objects.filter(pk = next_team.pk).update(role = 'RUNNER')      
            
            Team.objects.filter(game_id = current_game, role="CHASER").update(jail_time_start=datetime.now(), jail_time = 5)
            
            if response.get("challenge_pk", None) != None:
                challenge_pk = response.get("challenge_pk", None)
                challenge = Challenge.objects.get(pk=challenge_pk)
                ChallengeDoneByTeam.objects.filter(challenge=challenge, team=current_team).update(successful=False, open=False, timestamp_end=datetime.now())
                
            
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

        elif event == 'PENALTY-OVER':
            game = Game.objects.get(game_id = game_id)
            Team.objects.filter(game = game, team_name = send_team).update(jail_time_start='', jail_time = '')

        elif event == "HOP-ON":
            stops = response.get("stops", None)
            transport_type_id = response.get("transport_type_id", None)

            game = Game.objects.get(game_id = game_id)
            team = Team.objects.get(game = game, team_name = send_team)
            transport_type = TransportType.objects.get(pk = transport_type_id)

            cost_of_ride = transport_type.cost_per_station * stops
            team.coins -= cost_of_ride
            team.save()

            TransportDoneByTeam.objects.create(transport_type = transport_type,
                                               team = team,
                                               stops = stops,
                                               timestamp = datetime.now())

            self.send(text_data=json.dumps({
                "event": event,
                "send_team": send_team,
                "send_team_coins": team.coins,
            }))
        
        elif event == "UPDATE-POINTS":
            game = Game.objects.get(game_id = game_id)
            team = Team.objects.get(game = game, team_name = send_team, role="RUNNER")            
            
            team.points += 1
            team.save()

            other_team_points = Team.objects.filter(game = game).exclude(team_name = send_team).values_list("points", flat=True)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'update_points',
                    'event': event,
                    'game_id': game_id,
                    'send_team': send_team,
                    'send_team_points': team.points,
                    'other_team_points': list(other_team_points)
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

    def update_points(self, response):
        event = response["event"]
        send_team = response["send_team"]
        send_team_points = response["send_team_points"]
        other_team_points = response["other_team_points"]

        self.send(text_data=json.dumps({
            "send_team": send_team,
            "event": event,
            "send_team_points": send_team_points,
            "other_team_points": other_team_points
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
        
    
    
