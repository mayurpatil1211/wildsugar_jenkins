# Generated by Django 4.1 on 2023-11-17 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0026_reciperegistration_approved_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_types', models.CharField(max_length=50)),
                ('store_type_description', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand')),
            ],
            options={
                'db_table': 'store_type',
            },
        ),
    ]
