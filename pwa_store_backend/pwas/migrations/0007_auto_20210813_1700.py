# Generated by Django 3.1.13 on 2021-08-13 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pwas', '0006_auto_20210813_0813'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('name',)},
        ),
    ]