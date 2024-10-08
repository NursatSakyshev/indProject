from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_registration, name='user_registration'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/follow/', views.follow_user, name='follow_user'),
    path('profile/unfollow/', views.unfollow_user, name='unfollow_user'),
]
