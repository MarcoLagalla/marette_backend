# Generated by Django 3.0.6 on 2020-05-20 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20200520_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='restaurant_category',
            field=models.CharField(choices=[('Pizzeria', 'Pizzeria'), ('Ristorante', 'Ristorante'), ('Fast food', 'Fast food'), ('Gourmet', 'Gourmet'), ('Birrificio', 'Birrificio'), ('Mensa', 'Mensa'), ('Paninoteca', 'Paninoteca'), ('Bar', 'Bar'), ('Piadineria', 'Piadineria'), ('Osteria', 'Osteria'), ('Trattoria', 'Trattoria'), ('Tavola calda', 'Tavola calda'), ('Pasticceria', 'Pasticceria'), ('Cinese', 'Cinese'), ('All', 'All')], default='All', max_length=100),
            preserve_default=False,
        ),
    ]
