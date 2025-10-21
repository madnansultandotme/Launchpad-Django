from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Page

def user_home(request, username):
    user = get_object_or_404(User, username=username)
    pages = Page.objects.filter(user=user, is_published=True)
    return render(request, 'pages/root_home.html', {'user_profile': user, 'pages': pages})


def user_page(request, username, slug):
    user = get_object_or_404(User, username=username)
    page = get_object_or_404(Page, user=user, slug=slug, is_published=True)
    return render(request, 'pages/page_detail.html', {'user_profile': user, 'page': page})
   