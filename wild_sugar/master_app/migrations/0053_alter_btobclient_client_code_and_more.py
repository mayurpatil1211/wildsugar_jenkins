# Generated by Django 4.1 on 2024-03-01 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0052_alter_department_department_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btobclient',
            name='client_code',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='clusters',
            name='cluster_code',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='pos',
            name='pos_code',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
