# Generated by Django 3.0.4 on 2020-05-06 20:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0052_auto_20200506_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='iva',
            field=models.IntegerField(default=22, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
