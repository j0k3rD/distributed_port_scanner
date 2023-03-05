from django.urls import path
from .consumer import ScanConsumer

websocket_urlpatterns = [
    path('ws/scan/<str:groupkaname>/', ScanConsumer.as_asgi()),
]