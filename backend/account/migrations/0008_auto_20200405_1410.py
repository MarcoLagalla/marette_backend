# Generated by Django 3.0.4 on 2020-04-05 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20200405_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='birth_date',
            field=models.DateField(error_messages={'valid': '.'}),
        ),
    ]
