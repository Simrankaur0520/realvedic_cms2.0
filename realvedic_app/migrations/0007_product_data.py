# Generated by Django 4.1.5 on 2023-01-19 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realvedic_app', '0006_delete_product_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_id', models.TextField(blank=True)),
                ('Product_name', models.TextField(blank=True)),
                ('category', models.TextField(blank=True)),
                ('prices', models.TextField(blank=True)),
                ('Sizes', models.TextField(blank=True)),
                ('benefits', models.TextField(blank=True)),
                ('ingredients', models.TextField(blank=True)),
                ('how_to_use', models.TextField(blank=True)),
                ('how_we_make_it', models.TextField(blank=True)),
                ('nutrition', models.TextField(blank=True)),
                ('Status', models.TextField(blank=True)),
                ('sibling_product', models.TextField(blank=True)),
                ('HSN', models.TextField(blank=True)),
                ('SKU', models.TextField(blank=True)),
            ],
        ),
    ]
