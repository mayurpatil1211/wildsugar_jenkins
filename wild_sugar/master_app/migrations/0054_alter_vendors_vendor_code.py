# Generated by Django 4.1 on 2024-03-01 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0053_alter_btobclient_client_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendors',
            name='vendor_code',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
