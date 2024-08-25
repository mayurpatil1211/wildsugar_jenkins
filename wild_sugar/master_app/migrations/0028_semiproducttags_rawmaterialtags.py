# Generated by Django 4.1 on 2023-11-17 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0027_storetypes'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemiProductTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=140)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('semi_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semi_product_tags', to='master_app.semiproductregistrationmodel')),
            ],
            options={
                'db_table': 'semi_product_tags',
            },
        ),
        migrations.CreateModel(
            name='RawMaterialTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=140)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('raw_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_material_tags', to='master_app.rawmaterialregistrationmodel')),
            ],
            options={
                'db_table': 'raw_material_tags',
            },
        ),
    ]
