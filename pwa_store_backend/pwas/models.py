from django.conf import settings
from django.db.models import (
  CharField,
  SlugField,
  ForeignKey,
  CASCADE,
  ManyToManyField,
  OneToOneField,
  PositiveIntegerField,
  TextField,
  BooleanField
)
from django.db.models.signals import post_save
from pwa_store_backend.organizations.models import Organization
from django.core.validators import MaxValueValidator, MinValueValidator
from pwa_store_backend.utils.models import TimeStampAbstractModel, AbstractArchivedModel, OwnerAbstractModel


class Tag(TimeStampAbstractModel):
    name = CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('name',)
        unique_together = ['name']


class Pwa(TimeStampAbstractModel, AbstractArchivedModel, OwnerAbstractModel):
    name = CharField(max_length=50)
    url = CharField(max_length=250)
    slug = SlugField(null=True)
    organization = ForeignKey(
        Organization,
        related_name='organization',
        on_delete=CASCADE,
    )
    tags = ManyToManyField(
        Tag,
        related_name='tags',
    )

    image_url = CharField(max_length=250, null=True, blank=True)
    short_description = CharField(max_length=80, null=True, blank=True)
    description = TextField(max_length=1000, null=True, blank=True)
    published = BooleanField(default=False)  # to filter whether to show pwa in the marketplace

    def __str__(self):
        return self.name

    def get_tags(self):
        tags = self.tags.all()
        return ",\n".join([t.name for t in tags])

    class Meta:
        verbose_name = 'Pwa'
        verbose_name_plural = 'Pwas'
        ordering = ('name',)


class PwaScreenshot(TimeStampAbstractModel):
    pwa = ForeignKey(
        Pwa,
        related_name='pwa_screenshots',
        on_delete=CASCADE,
    )
    image_url = CharField(max_length=250, null=False)
    caption = CharField(max_length=80, null=False)

    class Meta:
        verbose_name = 'Pwa Screenshots'
        verbose_name_plural = 'Pwa Screenshots'

    def __str__(self):
        return self.pwa.name


class PwaAnalytics(TimeStampAbstractModel, AbstractArchivedModel):
    pwa = OneToOneField(Pwa, related_name='pwa_analytics', on_delete=CASCADE, null=False)
    view_count = PositiveIntegerField(default=0)
    launch_count = PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Pwa Analytics'
        verbose_name_plural = 'Pwa Analytics'

    def __str__(self):
        return self.pwa.name


class Rating(TimeStampAbstractModel, OwnerAbstractModel):
    pwa = ForeignKey(
        Pwa,
        related_name='ratings',
        on_delete=CASCADE,
    )
    value = PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = TextField(null=True)

    def __str__(self):
        return f"{self.created_by} | {self.pwa_id} | {self.value}"

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ('value',)
        unique_together = ['pwa', 'created_by']


class FavoritePwa(TimeStampAbstractModel, AbstractArchivedModel):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_favorites',
        on_delete=CASCADE,
    )
    pwa = ForeignKey(
        Pwa,
        related_name='pwa_favorites',
        on_delete=CASCADE,
    )

    def __str__(self):
        return self.pwa.name


# while working with signals imports should be at bottom to avoid circular signals
from pwa_store_backend.pwas.signals import pwa_post_save_handler
post_save.connect(pwa_post_save_handler, sender=Pwa)
