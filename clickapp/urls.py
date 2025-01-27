# myapp/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),
    path('increment_click_count/', views.increment_click_count, name='increment_click_count'), 
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('update_btext/', views.update_btext, name='update_btext'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]