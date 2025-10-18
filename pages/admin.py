from django.contrib import admin
from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
