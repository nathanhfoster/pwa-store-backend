# Generated by Django 3.1.13 on 2021-08-14 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pwas', '0016_auto_20210814_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pwa',
            name='launches',
        ),
        migrations.RemoveField(
            model_name='pwa',
            name='views',
        ),
    ]