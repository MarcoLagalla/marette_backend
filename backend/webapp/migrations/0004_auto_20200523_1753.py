# Generated by Django 3.0.4 on 2020-05-23 15:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20200523_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customervote',
            name='vote',
            field=models.PositiveIntegerField(validators=[django.core.validators.RegexValidator(regex='[0-5]{0}')]),
        ),
    ]
