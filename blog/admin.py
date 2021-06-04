from django.contrib import admin
from .models import Post, Commentary, OnlineUsers

admin.site.register(Post)
admin.site.register(Commentary)
admin.site.register(OnlineUsers)