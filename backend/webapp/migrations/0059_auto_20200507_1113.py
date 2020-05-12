# Generated by Django 3.0.4 on 2020-05-07 09:13

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0058_auto_20200507_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=False, null=True, quality=95, size=[300, 300], upload_to='restaurant'),
        ),
    ]