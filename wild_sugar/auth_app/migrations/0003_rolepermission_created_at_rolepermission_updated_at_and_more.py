# Generated by Django 4.1 on 2023-10-12 14:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_permissions_rolepermission_roles_userroles_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolepermission',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rolepermission',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userroles',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userroles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
