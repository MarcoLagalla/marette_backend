# Generated by Django 3.0.4 on 2020-05-03 13:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200426_1615'),
        ('webapp', '0038_auto_20200501_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('New', 'New'), ('Created', 'Created'), ('Confirmed', 'Confirmed'), ('Rejected', 'Rejected'), ('Payment Confirmed', 'Payment Confirmed'), ('Payment Declined', 'Payment Declined')], max_length=255)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('code', models.CharField(default='', max_length=6)),
                ('items', models.ManyToManyField(to='webapp.Product')),
                ('menus_items', models.ManyToManyField(to='webapp.Menu')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='shop', to='webapp.Restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='carts', to='account.Customer')),
            ],
        ),
    ]
