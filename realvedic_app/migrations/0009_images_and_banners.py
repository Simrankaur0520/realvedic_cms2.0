# Generated by Django 4.1.5 on 2023-01-20 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realvedic_app', '0008_rename_category_categoryy'),
    ]

    operations = [
        migrations.CreateModel(
            name='images_and_banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.TextField(auto_created=True)),
                ('title', models.TextField()),
                ('image', models.TextField()),
            ],
        ),
    ]
