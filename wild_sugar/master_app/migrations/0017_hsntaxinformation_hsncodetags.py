# Generated by Django 4.1 on 2023-09-17 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0016_finalproductregistrationmodel_brand_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HSNtaxInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hsn_code', models.CharField(max_length=240)),
                ('hsn_code_description', models.TextField(null=True)),
                ('cgst', models.FloatField(default=0)),
                ('sgst', models.FloatField(default=0)),
                ('igst', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_hsn_codes', to='master_app.brand')),
            ],
            options={
                'db_table': 'hsn_codes',
            },
        ),
        migrations.CreateModel(
            name='HSNcodeTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=240)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hsn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hsn_code_tags', to='master_app.hsntaxinformation')),
            ],
            options={
                'db_table': 'hsn_code_tags',
            },
        ),
    ]
