# Generated by Django 3.1.13 on 2021-08-07 19:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='contributors',
            field=models.ManyToManyField(related_name='organizationContributors', to=settings.AUTH_USER_MODEL),
        ),
    ]
