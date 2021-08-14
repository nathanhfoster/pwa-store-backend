from django.db import models
from django.conf import settings
from pwa_store_backend.organizations.models import Organization
from django.core.validators import MaxValueValidator, MinValueValidator 
from pwa_store_backend.utils.models import TimeStampAbstractModel, AbstractArchivedModel, OwnerAbstractModel

class Tag(models.Model):
    name = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('-name',)
        unique_together = ['name']

class Pwa(TimeStampAbstractModel, AbstractArchivedModel, OwnerAbstractModel):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=250)
    slug = models.SlugField(null=True)
    organization = models.ForeignKey(
        Organization,
        related_name='organization',
        on_delete=models.CASCADE,)

    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
    )

    icon_url = models.CharField(max_length=250, null=True, blank=True)
    short_description = models.CharField(max_length=80, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    launches = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False) # to filter whether to show pwa in the marketplace

    def __str__(self):
        return self.name

    def get_tags(self):
        tags = self.tags.all()
        return ",\n".join([t.name for t in tags])

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner} | {self.pwa_id} | {self.value}"

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ('-value',)
        unique_together = ['pwa_id', 'owner']