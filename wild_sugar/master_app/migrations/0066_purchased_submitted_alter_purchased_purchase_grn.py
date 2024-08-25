# Generated by Django 4.1 on 2024-04-10 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0065_alter_purchased_grn_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchased',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchased',
            name='purchase_grn',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
