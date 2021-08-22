# Generated by Django 3.1.13 on 2021-08-22 05:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pwas', '0034_merge_20210821_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='pwa',
            name='manifest_json',
            field=models.TextField(null=True, validators=[django.core.validators.MinLengthValidator(15)]),
        ),
        migrations.AddField(
            model_name='pwa',
            name='manifest_url',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
        migrations.AlterField(
            model_name='pwa',
            name='url',
            field=models.CharField(max_length=250, validators=[django.core.validators.MinLengthValidator(13)]),
        ),
    ]