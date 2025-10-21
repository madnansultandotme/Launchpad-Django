from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Page, SiteConfiguration
from launchpad.forms import SiteConfigurationForm, TailwindPageForm


def published_pages(request, username):
    user = User.objects.filter(username__iexact=username).first()
    pages = Page.objects.filter(user=user, is_published=True)
    site_config = None
    theme_class = 'bg-slate-900/40'
    if user:
        site_config = SiteConfiguration.objects.filter(user=user).first()
        if site_config:
            theme_class = (
                'bg-slate-900/40'
                if site_config.default_theme == SiteConfiguration.THEME_CLASSIC
                else 'bg-slate-950/30'
            )
    context = {
        'user_profile': user,
        'pages': pages,
        'site_config': site_config,
        'theme_class': theme_class,
    }
    return render(request, 'published_pages.html', context)


def page_detail(request, username, page_slug):
    user = User.objects.filter(username=username).first()
    # slug is unique 
    page = Page.objects.filter(user=user, slug=page_slug, is_published=True).first()
    site_config = SiteConfiguration.objects.filter(user=user).first() if user else None
    theme = site_config.default_theme if site_config else SiteConfiguration.THEME_MINIMAL
    return render(
        request,
        'page.html',
        {
            'user_profile': user,
            'page': page,
            'site_config': site_config,
            'theme': theme,
        },
    )


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


@login_required
def site_settings(request):
    config, _ = SiteConfiguration.objects.get_or_create(user=request.user)
    form = SiteConfigurationForm(request.POST or None, instance=config, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your site settings have been updated.')
        return redirect('site_settings')
    pages_count = Page.objects.filter(user=request.user).count()
    return render(
        request,
        'site_settings.html',
        {
            'form': form,
            'pages_count': pages_count,
        },
    )
       