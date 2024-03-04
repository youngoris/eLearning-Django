from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage_view, name='home'),
    path('search/', views.search_results, name='search_results'),
]
