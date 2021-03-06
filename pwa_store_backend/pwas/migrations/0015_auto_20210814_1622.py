# Generated by Django 3.1.13 on 2021-08-14 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pwas', '0014_auto_20210814_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='pwa_id',
            new_name='pwa',
        ),
        migrations.AddField(
            model_name='rating',
            name='comment',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='rating',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rating_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rating',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rating_updator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rating',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('pwa', 'created_by')},
        ),
        migrations.RemoveField(
            model_name='rating',
            name='owner',
        ),
    ]
