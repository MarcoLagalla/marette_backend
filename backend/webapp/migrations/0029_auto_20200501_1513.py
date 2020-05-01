# Generated by Django 3.0.4 on 2020-05-01 13:13

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0028_auto_20200501_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homecomponent',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='jpg', keep_meta=True, quality=100, size=[1920, 1080], upload_to='components/home'),
        ),
    ]