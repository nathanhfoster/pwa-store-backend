# Generated by Django 3.2.6 on 2021-08-28 14:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pwas', '0045_alter_pwa_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pwa',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
