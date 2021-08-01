from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Allow Spaces in User names

class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'

class User(AbstractUser):
    picture = models.TextField(blank=True)
    uploaded_picture = models.ImageField(blank=True, null=True)
    username_validator = MyValidator()
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username or email already exists."),
        },
    )
    email = models.EmailField(unique=True)
    opt_in = models.BooleanField(blank=True, default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-username',)
        unique_together = ('email',)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
    pass

    @property
    def get_picture(self):
        return self.uploaded_picture
