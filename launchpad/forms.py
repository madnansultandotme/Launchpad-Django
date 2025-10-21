from typing import cast

from django import forms
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import LoginForm, SignupForm
from dashboard.models import Page, SiteConfiguration


class TailwindFormMixin:
    """Apply shared Tailwind-friendly styling to AllAuth forms."""

    input_class = (
        'w-full rounded-xl border border-slate-700 bg-slate-900/80 px-4 py-3 '
        'text-slate-100 placeholder-slate-500 focus:border-blue-400 '
        'focus:outline-none focus:ring-2 focus:ring-blue-500/60'
    )
    checkbox_class = (
        'h-4 w-4 rounded border border-slate-700 bg-slate-900 text-blue-500 '
        'focus:outline-none focus:ring-2 focus:ring-blue-500/60'
    )

    def _init_tailwind(self) -> None:
        for name, field in self.fields.items():  # type: ignore[attr-defined]
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput)):
                widget.attrs['class'] = self.checkbox_class
            else:
                existing = widget.attrs.get('class', '')
                widget.attrs['class'] = f"{existing} {self.input_class}".strip()
                widget.attrs.setdefault('placeholder', field.label)
            field.label_suffix = ''


class TailwindSignupForm(TailwindFormMixin, SignupForm):
    field_order = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_tailwind()
        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = _(
            'Use at least 8 characters and avoid reusing old passwords.'
        )
        self.fields['password2'].help_text = _('Repeat your password to confirm.')


class TailwindLoginForm(TailwindFormMixin, LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_tailwind()
        login_label = _('Email or username')
        self.fields['login'].label = login_label
        self.fields['login'].widget.attrs['placeholder'] = login_label
        self.fields['password'].widget.attrs['placeholder'] = _('Password')
        if 'remember' in self.fields:
            self.fields['remember'].label = _('Keep me signed in')


class TailwindPageForm(TailwindFormMixin, forms.ModelForm):
    """Tailwind-styled form for the Page model."""

    class Meta:
        model = Page
        fields = ['title', 'slug', 'content', 'is_published']
        labels = {
            'title': _('Page Title'),
            'slug': _('Page Slug'),
            'content': _('Page Content'),
            'is_published': _('Publish this page?'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_tailwind()
        # Optional: Add placeholder text
        self.fields['title'].widget.attrs['placeholder'] = _('Enter a catchy page title')
        self.fields['slug'].widget.attrs['placeholder'] = _('Slug (optional) - same as title')
        self.fields['content'].widget.attrs['placeholder'] = _('Write your content here...')
        

class SiteConfigurationForm(TailwindFormMixin, forms.ModelForm):
    """Tailwind-styled form for managing a user's site configuration."""

    class Meta:
        model = SiteConfiguration
        fields = ['featured_page', 'site_title', 'site_description', 'default_theme']
        labels = {
            'featured_page': _('Select Site'),
            'site_title': _('Site Title'),
            'site_description': _('Tagline or Bio'),
            'default_theme': _('Default Theme'),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_tailwind()
        featured_page_field = cast(forms.ModelChoiceField, self.fields['featured_page'])
        existing_classes = featured_page_field.widget.attrs.get('class', '')
        featured_page_field.widget.attrs['class'] = (
            f"{existing_classes} bg-slate-900/70 border border-slate-700 rounded-md px-3 py-2 text-slate-100"
        ).strip()
        featured_page_field.required = False
        if user is not None:
            featured_page_field.queryset = Page.objects.filter(user=user)
        featured_page_field.empty_label = _('Select a page (optional)')
        self.fields['site_title'].widget.attrs['placeholder'] = _('My Launchpad Site')
        self.fields['site_description'].widget.attrs['placeholder'] = _('Share a short tagline for your site')

