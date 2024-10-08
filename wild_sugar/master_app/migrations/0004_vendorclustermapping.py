# Generated by Django 4.1 on 2023-08-20 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0003_pos_vendors_alter_departmentclustermapping_table_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorClusterMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendors', to='master_app.clusters')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clusters', to='master_app.vendors')),
            ],
            options={
                'db_table': 'vendor_cluster_mapping',
            },
        ),
    ]
