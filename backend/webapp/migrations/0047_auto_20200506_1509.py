# Generated by Django 3.0.4 on 2020-05-06 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0046_auto_20200505_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdiscount',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_discount', to='webapp.Restaurant'),
        ),
        migrations.AlterUniqueTogether(
            name='productdiscount',
            unique_together={('restaurant', 'title', 'type', 'value')},
        ),
        migrations.CreateModel(
            name='RestaurantDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Fisso', 'Fisso'), ('Percentuale', 'Percentuale'), ('All', 'All')], max_length=30)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_discount', to='webapp.Restaurant')),
            ],
        ),
    ]