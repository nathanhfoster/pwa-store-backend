from django.db import models
from django.conf import settings
from organizations.models import Organization


class Pwa(models.Model):
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    slug = models.SlugField(null=True)
    organization = models.ForeignKey(
        Organization,
        related_name='pwaOwner',
        on_delete=models.CASCADE,)

    description = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)