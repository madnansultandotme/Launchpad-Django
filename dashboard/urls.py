from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_pages, name='all_pages'),
    path('add-page/', views.add_page, name='add_page'),
    path('delete-page/<int:page_id>/', views.delete_page, name='delete_page'),
    path('edit-page/<int:page_id>/', views.edit_page, name='edit_page'),

]