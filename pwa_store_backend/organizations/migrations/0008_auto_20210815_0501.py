# Generated by Django 3.1.13 on 2021-08-15 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0007_auto_20210814_1745'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ('name',), 'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
    ]