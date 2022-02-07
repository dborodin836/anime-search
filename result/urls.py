from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<int:anime_id>', views.detail, name='detail'),
    path('random', views.random, name='random'),
]
