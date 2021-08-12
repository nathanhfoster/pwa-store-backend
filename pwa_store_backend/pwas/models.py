from django.db import models
from django.conf import settings
from pwa_store_backend.organizations.models import Organization

class Tag(models.Model):
    name = models.CharField(max_length=250)

    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('-name',)


class Pwa(models.Model):
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    slug = models.SlugField(null=True)
    organization = models.ForeignKey(
        Organization,
        related_name='pwaOwner',
        on_delete=models.CASCADE,)

    tags = models.ManyToManyField(
        Tag,
        related_name='pwaTags',)

    description = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        # app_label = 'pwas'
        verbose_name = 'Pwa'
        verbose_name_plural = 'Pwas'
        ordering = ('-name',)