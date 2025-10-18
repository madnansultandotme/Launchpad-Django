"""
URL configuration for launchpad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from dashboard import views as dashboard_views
from . import home_view

urlpatterns = [
    path('', home_view.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
     path('', include('pages.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/pages/', include('dashboard.urls')),

    path('<str:username>/', dashboard_views.published_pages, name='published_pages'),
    path('<str:username>/<str:page_slug>/', dashboard_views.page_detail, name='page_detail'),
]

# 👇 Add this only if you are using django-browser-reload
urlpatterns += [
    path("__reload__/", include("django_browser_reload.urls")),
]
