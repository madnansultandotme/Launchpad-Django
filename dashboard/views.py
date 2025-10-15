from django.shortcuts import render
from .models import Page
from launchpad.forms import TailwindPageForm
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError


def published_pages(request, username):
    user = User.objects.filter(username__iexact=username).first()
    pages = Page.objects.filter(user=user, is_published=True)
    return render(request, 'published_pages.html', {'user_profile': user, 'pages': pages})


def page_detail(request, username, page_slug):
    user = User.objects.filter(username=username).first()
    # slug is unique 
    page = Page.objects.filter(user=user, slug=page_slug, is_published=True).first()
    return render(request, 'page.html', {'user_profile': user, 'page': page})


@login_required
def all_pages(request):
    query = request.GET.get("q", "")
    pages = Page.objects.filter(user=request.user)
    if query:
        pages = pages.filter(title__icontains=query) | pages.filter(slug__icontains=query)
    return render(request, 'all_pages.html', {'pages': pages, 'query': query})

@login_required
def add_page(request):
    form = TailwindPageForm()
    if request.method == 'POST':
        form = TailwindPageForm(request.POST)
        if form.is_valid():
            try:
                page = form.save(commit=False)
                page.user = request.user
                page.save()
                return redirect('all_pages')
            except IntegrityError:
                # Handle unique constraint violation (slug already exists)
                form.add_error('slug', "This slug already exists.Use a different Slug or Title")  # Redirect to the list of pages after adding
    return render(request, 'add_page.html', {'form': form})

@login_required
@require_POST
def delete_page(request, page_id):
    try:
        page = Page.objects.get(id=page_id, user=request.user)
        page.delete()
    except Page.DoesNotExist:
            pass 
    return redirect('all_pages')  

@login_required
def edit_page(request, page_id):
    try:
        page = Page.objects.get(id=page_id, user=request.user)
    except Page.DoesNotExist:
        return redirect('all_pages')  # Redirect if the page does not exist or does not belong to the user

    form = TailwindPageForm(instance=page)

    if request.method == 'POST':
        form = TailwindPageForm(request.POST, instance=page)
        if form.is_valid():
            try:
                form.save()
                return redirect('all_pages')  
            except IntegrityError:
                form.add_error('slug', "This slug already exists. Use a different one.")
    return render(request, 'edit_page.html', {'form': form, 'page': page})
       