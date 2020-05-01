# Generated by Django 3.0.4 on 2020-05-01 13:42

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0031_auto_20200501_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='homecomponent',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homecomponent',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=False, null=True, quality=95, size=[1920, 1080], upload_to='components/home'),
        ),
    ]
