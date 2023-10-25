from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/oursystem/course/join_video_meeting/$', consumers.ChatConsumer.as_asgi()),
]
