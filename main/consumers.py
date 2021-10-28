from channels.generic.websocket import WebsocketConsumer
from main.models import Message,Room
from asgiref.sync import async_to_sync
import json


class ChatConsumer(WebsocketConsumer):
   
    def connect(self):


       
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        self.room_obj = Room.objects.get(room_name=self.room_name)



        async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
        )



 
        self.accept()
        

   
    def receive(self, text_data):
        reply = json.loads(text_data)

       
        self.messg = Message(room = self.room_obj,message=reply['message'],sender=reply['sender'])
        self.messg.save()
        print(reply)
     
      
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': reply
            }
        )

    def disconnect(self,*args,**kwargs):
        print("disconnected")

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({"reply": message}))            

