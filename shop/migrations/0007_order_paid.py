# Generated by Django 4.2.4 on 2023-08-28 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_bouquet_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Оплачено'),
        ),
    ]
