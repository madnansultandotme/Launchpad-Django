from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Page(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pages")
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = self.slug.lower()
        else:
            self.slug = slugify(self.title)
            
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} - {self.user.username}"


class SiteConfiguration(models.Model):
    THEME_MINIMAL = "minimal"
    THEME_CLASSIC = "classic"
    THEME_CHOICES = [
        (THEME_MINIMAL, "Minimal"),
        (THEME_CLASSIC, "Classic"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="site_configuration")
    site_title = models.CharField(max_length=150, blank=True)
    site_description = models.TextField(blank=True)
    default_theme = models.CharField(max_length=20, choices=THEME_CHOICES, default=THEME_MINIMAL)
    featured_page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        related_name="featured_on_configs",
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configurations"

    def __str__(self):
        return f"Site configuration for {self.user.username}"

    @property
    def resolved_title(self) -> str:
        if self.site_title:
            return self.site_title
        return f"{self.user.username}'s Launchpad"

    @property
    def resolved_description(self) -> str:
        if self.site_description:
            return self.site_description
        return "Welcome to my Launchpad profile."

