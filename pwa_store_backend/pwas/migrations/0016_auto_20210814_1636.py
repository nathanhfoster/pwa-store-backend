# Generated by Django 3.1.13 on 2021-08-14 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pwas', '0015_auto_20210814_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pwa',
            name='tags',
        ),
        migrations.AddField(
            model_name='pwa',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='pwas.Tag'),
        ),
    ]
