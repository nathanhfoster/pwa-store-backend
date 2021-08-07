from django.db import models
from django.conf import settings


class Organization(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='organizationOwner',
        on_delete=models.CASCADE,)

    description = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)