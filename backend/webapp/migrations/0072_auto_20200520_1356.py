# Generated by Django 3.0.6 on 2020-05-20 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0071_auto_20200520_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='restaurant',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.IntegerField(null=True),
        ),
    ]
