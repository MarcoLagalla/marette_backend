# Generated by Django 3.0.4 on 2020-05-23 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0014_auto_20200523_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='customer_vote_list',
        ),
    ]
