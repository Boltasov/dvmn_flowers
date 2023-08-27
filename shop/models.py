import os

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from telegram import Bot
from textwrap import dedent
from dotenv import load_dotenv


class Event(models.Model):
    """События, к которым заказывают букеты."""
    name = models.CharField(max_length=30, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Bouquet(models.Model):
    """Букеты"""
    name = models.CharField(
        max_length=30,
        verbose_name='Название'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    composition = models.TextField(
        verbose_name='Состав'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    size = models.TextField(
        verbose_name='Размер'
    )
    events = models.ManyToManyField(
        Event,
        related_name='bouquets',
        verbose_name='Подходящие события'
    )
    photo = models.ImageField(
        verbose_name='Фото',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name} - {str(self.price)}р.'

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'


class Order(models.Model):
    """ Заказы """
    class Status(models.TextChoices):
        CREATED = 'NEW', 'Создан'
        PAID = 'PAID', 'Оплачен'
        DONE = 'DONE', 'Доставлен'

    client_name = models.CharField(
        max_length=50,
        verbose_name='Имя клиента'
    )
    phone = models.CharField(
        max_length=10,
        verbose_name='Телефон'
    )  # Пока не стал запариваться с phone_number
    address = models.CharField(
        max_length=150,
        verbose_name='Адрес доставки'
    )
    datetime_created = models.DateTimeField(
        verbose_name='Дата создания заказа',
        auto_now_add=True,
    )
    deliver = models.DateTimeField(
        verbose_name='Дата и время доставки',
        blank=True,
        null=True,
    )
    bouquet = models.ManyToManyField(
        Bouquet,
        related_name='orders',
    )
    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status.CREATED
    )
    paid = models.BooleanField(
        default=False,
        verbose_name='Оплачено'
    )

    def __str__(self):
        return f'Заказ {self.pk} - {self.bouquet}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-datetime_created']
        indexes = [
            models.Index(fields=['-datetime_created', 'address']),
        ]

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        if self.paid:
            load_dotenv()
            tg_bot_key = os.getenv('TG_BOT_KEY')
            user_id = os.getenv('CHAT_ID')
            bot = Bot(token=tg_bot_key)
            message = f'''\
                        Новый заказ
    
                        Клиент: {self.client_name}
                        Адрес: {self.address}
                        Телеффон: {self.phone} '''
            bot.send_message(text=dedent(message), chat_id=user_id)


class Consultation(models.Model):
    """ Заявки на консультацию """
    client_name = models.CharField(
        max_length=50,
        verbose_name='Имя клиента'
    )
    phone = PhoneNumberField(
        verbose_name='Телефон'
    )
    datetime_created = models.DateTimeField(
        verbose_name='Дата создания заказа',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Консультация {self.pk} - {self.client_name}'

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'
