# Generated by Django 3.0.4 on 2020-05-06 20:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0051_product_iva'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='iva',
            field=models.IntegerField(default=22, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]