# Generated by Django 4.1 on 2023-10-19 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0022_department_brand_departmentclustermapping_food_cost_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='updated_date',
            new_name='updated_at',
        ),
        migrations.RemoveField(
            model_name='storeemployee',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='storeemployee',
            name='updated_date',
        ),
    ]
