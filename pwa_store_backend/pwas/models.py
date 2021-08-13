from django.db import models
from django.conf import settings
from pwa_store_backend.organizations.models import Organization
from django.core.validators import MaxValueValidator, MinValueValidator 

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
        unique_together = ['name']

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
    views = models.PositiveIntegerField(default=0)
    launches = models.PositiveIntegerField(default=0)

    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Pwa'
        verbose_name_plural = 'Pwas'
        ordering = ('-name',)

class Rating(models.Model):
    pwa_id = models.ForeignKey(
        Pwa,
        related_name='ratings',
        on_delete=models.CASCADE,)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='ratingOwner',
        on_delete=models.CASCADE,)
    
    value = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner} | {self.pwa_id} | {self.value}"

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ('-value',)
        unique_together = ['pwa_id', 'owner']