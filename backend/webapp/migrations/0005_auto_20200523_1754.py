# Generated by Django 3.0.4 on 2020-05-23 15:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20200523_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customervote',
            name='vote',
            field=models.PositiveIntegerField(validators=[django.core.validators.RegexValidator(regex='[0-5]{1}')]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='restaurant_rank',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.RegexValidator(regex='[0-5]{1}')]),
        ),
    ]
