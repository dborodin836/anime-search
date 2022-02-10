from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
    path('<int:anime_id>', views.DetailView.as_view(), name='detail'),
    path('random', views.RandomAnimeRedirect.as_view(), name='random'),
]
