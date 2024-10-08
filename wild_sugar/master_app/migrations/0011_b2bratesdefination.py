# Generated by Django 4.1 on 2023-09-03 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0010_alter_vendorbankdetails_account_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='B2BRatesDefination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=50)),
                ('item_name', models.CharField(max_length=250)),
                ('unit_of_measurement', models.CharField(max_length=50)),
                ('rate', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'b2b_rates_defination',
            },
        ),
    ]
