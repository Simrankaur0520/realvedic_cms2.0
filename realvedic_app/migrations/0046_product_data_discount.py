# Generated by Django 4.0.3 on 2023-02-16 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realvedic_app', '0045_images_and_banners_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_data',
            name='discount',
            field=models.TextField(blank=True),
        ),
    ]
