# Generated by Django 3.0.4 on 2020-05-08 10:06

import backend.webapp.models.components
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0063_order_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homecomponent',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=False, null=True, quality=95, size=[1920, 1080], upload_to=backend.webapp.models.components.home_component),
        ),
    ]
