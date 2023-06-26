import json
from channels.generic.websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        
        self.send(text_data=json.dumps({
            "type": "connection_established",
            "message": "You are now connected!"
        }))

    # def receive(self, event):
    #     self.send({
    #         "type": "websocket.send",
    #         "text": event["text"],
    #     })

    # 
