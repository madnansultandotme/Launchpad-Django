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

