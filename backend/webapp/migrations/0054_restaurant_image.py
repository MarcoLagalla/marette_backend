# Generated by Django 3.0.4 on 2020-05-07 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0053_menu_iva'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='restaurant'),
        ),
    ]