# Generated by Django 4.1 on 2024-02-21 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0051_pomodel_poitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_uid',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
