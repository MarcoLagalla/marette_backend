# Generated by Django 3.0.4 on 2020-04-05 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200405_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='birth_date',
            field=models.DateField(),
        ),
    ]
