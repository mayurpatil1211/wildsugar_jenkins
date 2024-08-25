# Generated by Django 4.1 on 2024-08-08 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('master_app', '0080_ordersheet_delivery_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocktransfer',
            name='received_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_by_stock_transfer', to=settings.AUTH_USER_MODEL),
        ),
    ]
