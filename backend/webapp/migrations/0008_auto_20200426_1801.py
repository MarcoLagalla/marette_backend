# Generated by Django 3.0.4 on 2020-04-26 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20200426_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuentry',
            name='product',
        ),
        migrations.AddField(
            model_name='menuentry',
            name='products',
            field=models.ManyToManyField(blank=True, to='webapp.Product'),
        ),
        migrations.AddField(
            model_name='menuentry',
            name='restaurant',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='webapp.Restaurant'),
            preserve_default=False,
        ),
    ]
