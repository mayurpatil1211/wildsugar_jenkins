# Generated by Django 4.1 on 2023-09-02 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0009_btobclient_alter_poscompanymapping_unique_together_and_more'),
    ]

    operations = [
        
        migrations.CreateModel(
            name='B2BclientPOSMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pos', to='master_app.btobclient')),
                ('pos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='master_app.pos')),
            ],
            options={
                'db_table': 'client_pos_mapping',
            },
        ),
        migrations.CreateModel(
            name='B2BclientClusterMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clusters', to='master_app.btobclient')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='master_app.clusters')),
            ],
            options={
                'db_table': 'client_cluster_mapping',
            },
        ),
        migrations.CreateModel(
            name='B2BclientBrandMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='master_app.brand')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='master_app.btobclient')),
            ],
            options={
                'db_table': 'client_brand_mapping',
            },
        ),
    ]
