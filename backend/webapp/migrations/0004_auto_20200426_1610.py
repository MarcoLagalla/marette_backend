# Generated by Django 3.0.4 on 2020-04-26 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20200426_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Altro', 'Altro'), ('Antipasto', 'Antipasto'), ('Contorno', 'Contorno'), ('Dessert', 'Dessert'), ('Caffetteria', 'Caffetteria'), ('Panetteria', 'Panetteria'), ('Panini e Piadine', 'Panini e Piadine'), ('Pizza', 'Pizza'), ('Primo', 'Primo'), ('Secondo', 'Secondo'), ('Snack', 'Snack')], max_length=30),
        ),
    ]