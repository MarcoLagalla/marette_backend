# Generated by Django 3.0.6 on 2020-05-20 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0073_auto_20200520_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='n_civ',
            field=models.CharField(max_length=10),
        ),
    ]
