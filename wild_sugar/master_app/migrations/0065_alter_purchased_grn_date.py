# Generated by Django 4.1 on 2024-04-06 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0064_btobclient_is_msme_registered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchased',
            name='grn_date',
            field=models.DateField(null=True),
        ),
    ]
