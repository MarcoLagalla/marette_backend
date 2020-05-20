# Generated by Django 3.0.6 on 2020-05-20 12:56

import backend.account.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_activated', models.BooleanField(auto_created=True, default=False)),
                ('avatar', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=False, null=True, quality=95, size=[250, 250], upload_to=backend.account.models.content_file_name)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(error_messages={'unique': 'Esiste già un utente con questo numero.'}, max_length=128, region=None, unique=True)),
                ('activation_token', models.CharField(max_length=200, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_activated', models.BooleanField(auto_created=True, default=False)),
                ('avatar', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=False, null=True, quality=95, size=[250, 250], upload_to=backend.account.models.content_file_name)),
                ('cf', models.CharField(max_length=16, unique=True)),
                ('birth_date', models.DateField()),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=150)),
                ('n_civ', models.CharField(max_length=10)),
                ('cap', models.IntegerField(validators=[django.core.validators.RegexValidator(regex='[0-9]{5}')])),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(error_messages={'unique': 'Esiste già un utente con questo numero.'}, max_length=128, region=None, unique=True)),
                ('activation_token', models.CharField(max_length=200, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='business', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Businesses',
            },
        ),
    ]
