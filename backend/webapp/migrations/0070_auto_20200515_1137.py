# Generated by Django 3.0.6 on 2020-05-15 09:37

import backend.webapp.models.models
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0069_remove_galleriacomponent_immagini'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='PNG', keep_meta=False, quality=95, size=[600, 600], upload_to=backend.webapp.models.models.gallery_component),
        ),
    ]