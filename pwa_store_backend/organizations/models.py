from django.db import models
from django.conf import settings
from pwa_store_backend.utils.models import TimeStampAbstractModel, AbstractArchivedModel, OwnerAbstractModel

class Organization(TimeStampAbstractModel, AbstractArchivedModel, OwnerAbstractModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(null=True)

    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='organizationContributors',
    )
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_contributors(self):
        contributors = self.contributors.all()
        return ",\n".join([c.name for c in contributors])


    class Meta:
        # app_label = 'organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ('-name',)