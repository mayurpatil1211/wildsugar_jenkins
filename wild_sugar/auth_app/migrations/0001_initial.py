# Generated by Django 4.1 on 2023-08-15 06:09

import auth_app.manager
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, null=True, unique=True)),
                ('contact_number', models.CharField(blank=True, max_length=13, null=True)),
                ('user_type', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('active', models.BooleanField(default=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, default='India', max_length=100, null=True)),
                ('pan', models.CharField(blank=True, max_length=20, null=True)),
                ('adhar', models.CharField(blank=True, max_length=30, null=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('login_count', models.IntegerField(default=0)),
                ('blocked', models.BooleanField(default=False)),
                ('profile_picture_link', models.TextField(blank=True, null=True)),
                ('profile_picture_key', models.CharField(blank=True, max_length=100, null=True)),
                ('record_date', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
            },
            managers=[
                ('objects', auth_app.manager.UserManager()),
            ],
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username', 'email', 'active', 'record_date'], name='user_usernam_01b047_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username'], name='user_usernam_b79065_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='user_email_7bbb4c_idx'),
        ),
    ]
