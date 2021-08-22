# Generated by Django 3.1.13 on 2021-08-20 05:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_auto_20210815_0847'),
        ('pwas', '0029_auto_20210820_0449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pwa',
            name='name',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='pwa',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='organizations.organization'),
        ),
        migrations.AlterField(
            model_name='pwa',
            name='slug',
            field=models.SlugField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='pwa',
            name='url',
            field=models.CharField(max_length=250, validators=[django.core.validators.MinLengthValidator(15)]),
        ),
    ]