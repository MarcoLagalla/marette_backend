# Generated by Django 3.0.4 on 2020-05-07 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0057_auto_20200507_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='slug',
            field=models.SlugField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='url',
            field=models.CharField(blank=True, default='', max_length=150, null=True, unique=True),
        ),
    ]