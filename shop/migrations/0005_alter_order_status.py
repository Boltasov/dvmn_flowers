# Generated by Django 4.2.4 on 2023-08-26 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_consultation_datetime_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'Создан'), ('PAID', 'Оплачен'), ('DONE', 'Доставлен')], default='NEW', max_length=4),
        ),
    ]
