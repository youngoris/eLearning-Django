from django.urls import path
from . import views
from .consumers import ChatConsumer
from django.urls import re_path

urlpatterns = [
    path('', views.homepage_view, name='home'),
    path('search/', views.search_results, name='search_results'),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),

]
