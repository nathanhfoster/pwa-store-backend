# Generated by Django 3.1.13 on 2021-08-14 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pwas', '0011_auto_20210814_1217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='date_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='last_modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='date_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='last_modified',
            new_name='updated_at',
        ),
    ]