import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class GameConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = 'test'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        
        # self.send(text_data=json.dumps({
        #     "type": "connection_established",
        #     "message": "You are now connected!"
        # }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))
        # self.send(text_data=json.dumps({
        #     'type': 'chat',
        #     'message': message
        # }))
    # 

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

    def disconnect(self):
        print("Disconnected")

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
        
    
    def add_team(self, response):
        
        team_name = response["team_name"]
        event = response["event"]
        
        self.send(text_data=json.dumps({
            "team_name": team_name,
            "event": event,
        }))
