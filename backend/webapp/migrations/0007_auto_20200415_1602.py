# Generated by Django 3.0.4 on 2020-04-15 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20200415_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='C:\\Users\\Marco\\PycharmProjects\\marette_backend\\media'),
        ),
    ]
