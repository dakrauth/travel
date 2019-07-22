from django.urls import path
from . import views

urlpatterns = [
    path('logs/<str:username>/', views.UserLogListView.as_view(), name='user_log_api'),
    path('flag-game/', views.FlagGameView.as_view(), name='flag_game_api'),
]
