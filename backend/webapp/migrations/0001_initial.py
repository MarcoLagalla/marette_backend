# Generated by Django 3.0.6 on 2020-05-24 13:35

import backend.webapp.models.components
import backend.webapp.models.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContattaciComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('show', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_who_voted', to='account.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='EventiComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('show', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GalleriaComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('show', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HomeComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=False, null=True, quality=95, size=[1920, 1080], upload_to=backend.webapp.models.components.home_component)),
                ('description', models.TextField(blank=True, null=True)),
                ('show', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('iva', models.IntegerField(default=22, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='MenuComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('show', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='png', keep_meta=True, null=True, quality=0, size=[32, 32], upload_to='tag_icon')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, default='', null=True)),
                ('url', models.CharField(blank=True, default='', max_length=150, null=True, unique=True)),
                ('activity_name', models.CharField(max_length=30)),
                ('activity_description', models.TextField()),
                ('city', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('n_civ', models.CharField(max_length=10)),
                ('cap', models.PositiveIntegerField(validators=[django.core.validators.RegexValidator(regex='[0-9]{5}')])),
                ('restaurant_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('p_iva', models.CharField(max_length=11)),
                ('restaurant_category', models.CharField(choices=[('Pizzeria', 'Pizzeria'), ('Ristorante', 'Ristorante'), ('Fast food', 'Fast food'), ('Gourmet', 'Gourmet'), ('Birrificio', 'Birrificio'), ('Mensa', 'Mensa'), ('Paninoteca', 'Paninoteca'), ('Bar', 'Bar'), ('Piadineria', 'Piadineria'), ('Osteria', 'Osteria'), ('Trattoria', 'Trattoria'), ('Tavola calda', 'Tavola calda'), ('Pasticceria', 'Pasticceria'), ('Cinese', 'Cinese'), ('All', 'All')], max_length=100)),
                ('restaurant_rank', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='PNG', keep_meta=False, null=True, quality=95, size=[300, 300], upload_to='restaurant')),
                ('customer_vote_list', models.ManyToManyField(blank=True, related_name='customer_vote_list', to='webapp.CustomerVote')),
            ],
        ),
        migrations.CreateModel(
            name='VetrinaComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('show', models.BooleanField(default=False)),
                ('menu_giorno', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='menu_giorno', to='webapp.Menu')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vetrina', to='webapp.Restaurant')),
            ],
            options={
                'unique_together': {('restaurant', 'name')},
            },
        ),
        migrations.CreateModel(
            name='RestaurantDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Fisso', 'Fisso'), ('Percentuale', 'Percentuale')], max_length=30)),
                ('category', models.CharField(choices=[('Altro', 'Altro'), ('Antipasto', 'Antipasto'), ('Contorno', 'Contorno'), ('Dessert', 'Dessert'), ('Caffetteria', 'Caffetteria'), ('Panetteria', 'Panetteria'), ('Panini e Piadine', 'Panini e Piadine'), ('Pizza', 'Pizza'), ('Primo', 'Primo'), ('Secondo', 'Secondo'), ('Snack', 'Snack'), ('All', 'All')], max_length=100)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_discount', to='webapp.Restaurant')),
            ],
            options={
                'unique_together': {('restaurant', 'title', 'type', 'category', 'value')},
            },
        ),
        migrations.CreateModel(
            name='RestaurantComponents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contattaci', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='contattaci_component', to='webapp.ContattaciComponent')),
                ('eventi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='eventi_component', to='webapp.EventiComponent')),
                ('galleria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='galleria_component', to='webapp.GalleriaComponent')),
                ('home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='home_component', to='webapp.HomeComponent')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='menu_component', to='webapp.MenuComponent')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='webapp.Restaurant')),
                ('vetrina', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vetrina_component', to='webapp.VetrinaComponent')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='discounts',
            field=models.ManyToManyField(blank=True, related_name='rest_discounts', to='webapp.RestaurantDiscount'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='account.Business'),
        ),
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Fisso', 'Fisso'), ('Percentuale', 'Percentuale')], max_length=30)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_discount', to='webapp.Restaurant')),
            ],
            options={
                'unique_together': {('restaurant', 'title', 'type', 'value')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=600)),
                ('category', models.CharField(choices=[('Altro', 'Altro'), ('Antipasto', 'Antipasto'), ('Contorno', 'Contorno'), ('Dessert', 'Dessert'), ('Caffetteria', 'Caffetteria'), ('Panetteria', 'Panetteria'), ('Panini e Piadine', 'Panini e Piadine'), ('Pizza', 'Pizza'), ('Primo', 'Primo'), ('Secondo', 'Secondo'), ('Snack', 'Snack')], max_length=30)),
                ('image', models.ImageField(blank=True, null=True, upload_to=backend.webapp.models.models.products_image)),
                ('thumb_image', models.ImageField(blank=True, null=True, upload_to=backend.webapp.models.models.products_image_thumb)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('iva', models.IntegerField(default=22, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('show_image', models.BooleanField(blank=True, default=True)),
                ('available', models.BooleanField(blank=True, default=True)),
                ('discounts', models.ManyToManyField(blank=True, to='webapp.ProductDiscount')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='webapp.Restaurant')),
                ('tags', models.ManyToManyField(blank=True, to='webapp.ProductTag')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='PNG', keep_meta=False, quality=95, size=[600, 600], upload_to=backend.webapp.models.models.gallery_component)),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='webapp.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid', models.BooleanField(auto_created=True, default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('New', 'New'), ('Created', 'Created'), ('Confirmed', 'Confirmed'), ('Rejected', 'Rejected'), ('Payment Confirmed', 'Payment Confirmed'), ('Payment Declined', 'Payment Declined')], max_length=255)),
                ('code', models.CharField(blank=True, default='', max_length=100)),
                ('items', models.ManyToManyField(blank=True, to='webapp.Product')),
                ('menus_items', models.ManyToManyField(blank=True, to='webapp.Menu')),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop', to='webapp.Restaurant')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carts', to='account.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='MenuEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('num_products', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Menu')),
                ('products', models.ManyToManyField(blank=True, to='webapp.Product')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='menucomponent',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_component', to='webapp.Restaurant'),
        ),
        migrations.AddField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Restaurant'),
        ),
        migrations.AddField(
            model_name='homecomponent',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home', to='webapp.Restaurant'),
        ),
        migrations.AddField(
            model_name='galleriacomponent',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='galleria_component', to='webapp.Restaurant'),
        ),
        migrations.AddField(
            model_name='eventicomponent',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventi_component', to='webapp.Restaurant'),
        ),
        migrations.AddField(
            model_name='customervote',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_vote', to='webapp.Restaurant'),
        ),
        migrations.AddField(
            model_name='contattacicomponent',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contattaci_component', to='webapp.Restaurant'),
        ),
        migrations.AlterUniqueTogether(
            name='restaurant',
            unique_together={('id', 'owner', 'p_iva')},
        ),
        migrations.AlterUniqueTogether(
            name='menucomponent',
            unique_together={('restaurant', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='homecomponent',
            unique_together={('restaurant', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='galleriacomponent',
            unique_together={('restaurant', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='eventicomponent',
            unique_together={('restaurant', 'name')},
        ),
        migrations.AddConstraint(
            model_name='customervote',
            constraint=models.UniqueConstraint(fields=('customer', 'restaurant'), name='unique_vote_for_user_at_rest'),
        ),
        migrations.AlterUniqueTogether(
            name='contattacicomponent',
            unique_together={('restaurant', 'name')},
        ),
    ]
