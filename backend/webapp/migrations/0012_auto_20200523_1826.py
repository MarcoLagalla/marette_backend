# Generated by Django 3.0.4 on 2020-05-23 16:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_auto_20200523_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='restaurant_rank',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.RegexValidator(regex='^([0-5])$')]),
        ),
    ]
