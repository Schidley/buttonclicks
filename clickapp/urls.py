# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),
    path('increment_click_count/', views.increment_click_count, name='increment_click_count'), 
]