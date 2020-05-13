# Generated by Django 3.0.6 on 2020-05-12 19:36

import backend.webapp.models.models
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0066_auto_20200508_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='JPEG', keep_meta=False, quality=95, size=[600, 600], upload_to=backend.webapp.models.models.gallery_component),
        ),
    ]