# Generated by Django 4.1.5 on 2023-02-22 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realvedic_app', '0055_product_data_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True)),
                ('phone_no', models.TextField(blank=True)),
                ('email_id', models.TextField(blank=True)),
                ('password', models.TextField(blank=True)),
                ('token', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='user_data',
            name='user_type',
            field=models.TextField(default='User'),
        ),
    ]
