# Generated by Django 3.0.6 on 2020-05-12 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0066_auto_20200508_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('U', 'Unread'), ('R', 'Read')], max_length=1)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='webapp.Order')),
            ],
        ),
    ]
