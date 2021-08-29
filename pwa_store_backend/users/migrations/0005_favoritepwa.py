# Generated by Django 3.2.6 on 2021-08-29 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pwas', '0053_delete_favoritepwa'),
        ('users', '0004_auto_20210815_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoritePwa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived', models.BooleanField(default=False)),
                ('archived_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('pwa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pwa_favorites', to='pwas.pwa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]