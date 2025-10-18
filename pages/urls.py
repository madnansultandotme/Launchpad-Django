from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.user_home, name='user_home'),
    path('<str:username>/<slug:slug>/', views.user_page, name='user_page'),
]
