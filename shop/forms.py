from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget

from .models import Consultation


class ConsultationFortm(forms.Form):
    name = forms.CharField(
        max_length=25,
        widget=forms.widgets.TextInput(attrs={'class': 'order__form_input',
                                              'placeholder': 'Введите Имя'})
    )
    phone = PhoneNumberField(
        region='RU',
        widget=RegionalPhoneNumberWidget(region='RU', attrs={'class': 'order__form_input',
                                                             'placeholder': '+7 (999) 000 00 00'}),
    )
    checkbox = forms.BooleanField(required=True,
                                  widget=forms.CheckboxInput(),
                                  label='Я согласен(а) с политикой конфидециоальности',
                                  initial=True
                                  )