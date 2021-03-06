# Generated by Django 3.1.13 on 2021-08-14 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pwas', '0012_auto_20210814_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='PwaAnalytics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived', models.BooleanField(default=False)),
                ('archived_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('launch_count', models.PositiveIntegerField(default=0)),
                ('pwa', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pwa_analytics', to='pwas.pwa')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
