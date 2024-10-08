# Generated by Django 4.1 on 2023-10-06 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0019_b2bratesdefinition_delete_b2bratesdefination'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finalproductregistrationmodel',
            name='product_type',
        ),
        migrations.RemoveField(
            model_name='rawmaterialregistrationmodel',
            name='product_type',
        ),
        migrations.RemoveField(
            model_name='semiproductregistrationmodel',
            name='product_type',
        ),
        migrations.RemoveField(
            model_name='store',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='store',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='department',
            name='target_food_cost',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='finalproductregistrationmodel',
            name='high_value_item',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='rawmaterialregistrationmodel',
            name='high_value_item',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='semiproductregistrationmodel',
            name='high_value_item',
            field=models.BooleanField(null=True),
        ),
        
        migrations.CreateModel(
            name='RawMaterialPosMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_material', to='master_app.pos')),
                ('raw_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pos', to='master_app.rawmaterialregistrationmodel')),
            ],
            options={
                'db_table': 'raw_material_pos_mapping',
                'unique_together': {('raw_material', 'pos')},
            },
        ),
        migrations.CreateModel(
            name='RawMaterialDeptMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_material', to='master_app.department')),
                ('raw_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='master_app.rawmaterialregistrationmodel')),
            ],
            options={
                'db_table': 'raw_material_dept_mapping',
                'unique_together': {('raw_material', 'department')},
            },
        ),
        migrations.CreateModel(
            name='FinalProductPriceForPOS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('final_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_for_pos', to='master_app.finalproductregistrationmodel')),
                ('pos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_material_prices', to='master_app.pos')),
            ],
            options={
                'db_table': 'final_product_price_pos',
                'unique_together': {('final_product', 'pos')},
            },
        ),
    ]
