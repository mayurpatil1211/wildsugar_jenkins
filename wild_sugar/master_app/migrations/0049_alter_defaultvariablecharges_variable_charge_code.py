# Generated by Django 4.1 on 2024-02-05 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0048_defaultvariablecharges_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultvariablecharges',
            name='variable_charge_code',
            field=models.CharField(max_length=240),
        ),
    ]
