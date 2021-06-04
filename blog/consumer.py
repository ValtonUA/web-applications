import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.forms.models import model_to_dict
import datetime
from blog.models import OnlineUsers, Post, Commentary, User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = 'chat_%s' % self.post_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.post_group_name,
            self.channel_name
        )

        name = f"Anonymous - {self.scope['client'][1]}" \
            if self.scope['user'] == "" else self.scope['user']

        res = User.objects.filter(username=name)[0]
        OnlineUsers.objects.create(user=res)
        self.user = res
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.post_group_name,
            self.channel_name
        )
        OnlineUsers.objects.filter(user=self.user).delete()

    # # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)

        post = Post.objects.get(id=int(data_json['post_id']))
        name = f"Anonymous - {self.scope['client'][1]}" \
            if self.scope['user'] == "" else self.scope['user']

        res = User.objects.filter(username=name)[0]
        comment = Commentary(post=post, text=data_json['commentText'], author=res)
        comment.save()
        data_json = json.loads(json.dumps(model_to_dict(comment)))
        data_json['date'] = comment.date.strftime("%d.%m.%Y %H:%M")

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.post_group_name,
            {
                'type': 'chat_message',
                'entity_data': data_json
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        entity_data = event['entity_data']
        print(entity_data)
        # Send message to WebSocket
        self.send(text_data=json.dumps(entity_data))


class TasksConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "finished_tasks"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data_json)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'task_message',
                'message': message
            }
        )

    def task_message(self, event):
        message = event['message']
        print(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


