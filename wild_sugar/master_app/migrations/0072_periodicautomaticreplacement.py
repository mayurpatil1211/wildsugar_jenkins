# Generated by Django 4.1 on 2024-06-08 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0071_planningmaterialdistribution'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodicAutomaticReplacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200)),
                ('item_code', models.CharField(max_length=200)),
                ('default_uom', models.CharField(max_length=20)),
                ('default_uom_quantity', models.FloatField(default=0)),
                ('default_value_for_day', models.FloatField()),
                ('value_for_week_day', models.JSONField(default={'Fri': None, 'Mon': None, 'Sat': None, 'Sun': None, 'Thu': None, 'Tue': None, 'Wed': None})),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_par', to='master_app.department')),
                ('final_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='final_product_par', to='master_app.finalproductregistrationmodel')),
                ('pos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pos_par', to='master_app.pos')),
                ('raw_material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='raw_material_par', to='master_app.rawmaterialregistrationmodel')),
                ('semi_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='semi_product_par', to='master_app.semiproductregistrationmodel')),
            ],
            options={
                'db_table': 'periodic_automatic_replacement',
            },
        ),
    ]
