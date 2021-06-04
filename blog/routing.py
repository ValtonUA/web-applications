from django.urls import re_path, path

from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/blog/(?P<post_id>\w+)/$', consumer.ChatConsumer.as_asgi()),
    path('ws/blog/tasks/', consumer.TasksConsumer.as_asgi()),
]
