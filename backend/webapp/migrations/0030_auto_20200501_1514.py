# Generated by Django 3.0.4 on 2020-05-01 13:14

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0029_auto_20200501_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homecomponent',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, quality=100, size=[1920, 1080], upload_to='components/home'),
        ),
    ]
