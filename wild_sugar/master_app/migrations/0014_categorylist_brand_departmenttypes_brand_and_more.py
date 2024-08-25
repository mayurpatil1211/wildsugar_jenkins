# Generated by Django 4.1 on 2023-09-14 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0013_storeclustermapping_storebrandmapping_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorylist',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand'),
        ),
        migrations.AddField(
            model_name='departmenttypes',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand'),
        ),
        migrations.AddField(
            model_name='highvalueitemtypes',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand'),
        ),
        migrations.AddField(
            model_name='postypes',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand'),
        ),
        migrations.AddField(
            model_name='prioritiytypes',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand'),
        ),
        migrations.AddField(
            model_name='producttypes',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand'),
        ),
        migrations.AddField(
            model_name='severitytypes',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand'),
        ),
        migrations.AddField(
            model_name='subcategorylist',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand'),
        ),
        migrations.AddField(
            model_name='unitofmeasurement',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand'),
        ),
        migrations.AddField(
            model_name='vendortypes',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_app.brand'),
        ),
    ]
