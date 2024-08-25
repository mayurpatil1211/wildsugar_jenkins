# Generated by Django 4.1 on 2023-10-10 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_description', models.CharField(max_length=240)),
                ('permission_code', models.CharField(max_length=240)),
                ('in_action', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'permissions',
            },
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'role_permissions',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=240)),
                ('role_code', models.CharField(max_length=240)),
                ('in_action', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'roles',
            },
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to='auth_app.roles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_roles',
            },
        ),
        migrations.AddIndex(
            model_name='roles',
            index=models.Index(fields=['role_code', 'role_name'], name='roles_role_co_bcb150_idx'),
        ),
        migrations.AddIndex(
            model_name='roles',
            index=models.Index(fields=['role_code'], name='roles_role_co_be68ba_idx'),
        ),
        migrations.AddIndex(
            model_name='roles',
            index=models.Index(fields=['role_name'], name='roles_role_na_cfef50_idx'),
        ),
        migrations.AddIndex(
            model_name='roles',
            index=models.Index(fields=['in_action'], name='roles_in_acti_757fa7_idx'),
        ),
        migrations.AddField(
            model_name='rolepermission',
            name='permission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='auth_app.permissions'),
        ),
        migrations.AddField(
            model_name='rolepermission',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='auth_app.roles'),
        ),
        migrations.AddField(
            model_name='permissions',
            name='parent_permission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth_app.permissions'),
        ),
        migrations.AddIndex(
            model_name='userroles',
            index=models.Index(fields=['role'], name='user_roles_role_id_0b583b_idx'),
        ),
        migrations.AddIndex(
            model_name='userroles',
            index=models.Index(fields=['user'], name='user_roles_user_id_05df60_idx'),
        ),
        migrations.AddIndex(
            model_name='rolepermission',
            index=models.Index(fields=['role'], name='role_permis_role_id_0ea48f_idx'),
        ),
        migrations.AddIndex(
            model_name='rolepermission',
            index=models.Index(fields=['permission'], name='role_permis_permiss_96a6c9_idx'),
        ),
        migrations.AddIndex(
            model_name='permissions',
            index=models.Index(fields=['permission_code', 'parent_permission'], name='permissions_permiss_b856ed_idx'),
        ),
        migrations.AddIndex(
            model_name='permissions',
            index=models.Index(fields=['permission_code'], name='permissions_permiss_fee52e_idx'),
        ),
        migrations.AddIndex(
            model_name='permissions',
            index=models.Index(fields=['parent_permission'], name='permissions_parent__78f9f6_idx'),
        ),
        migrations.AddIndex(
            model_name='permissions',
            index=models.Index(fields=['permission_description'], name='permissions_permiss_82cf6d_idx'),
        ),
    ]
