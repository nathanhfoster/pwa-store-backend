# Generated by Django 3.1.13 on 2021-08-20 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_auto_20210815_0847'),
        ('pwas', '0028_auto_20210820_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pwa',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='organizations.organization'),
        ),
    ]