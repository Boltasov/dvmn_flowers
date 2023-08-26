from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget


class ConsultationFortm(forms.Form):
    name = forms.CharField(
        max_length=25,
        widget=forms.widgets.TextInput(attrs={'class': 'order__form_input',
                                              'placeholder': 'Введите Имя'})
    )
    phone = PhoneNumberField(
        region='RU',
        widget=RegionalPhoneNumberWidget(
            region='RU',
            attrs={'class': 'order__form_input',
                   'placeholder': '+7 (999) 000 00 00'}
        ),
    )
    checkbox = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(),
        label='Я согласен(а) с политикой конфиденциальности',
        initial=True
    )


class OrderForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        widget=forms.widgets.TextInput(attrs={'class': 'order__form_input',
                                              'placeholder': 'Введите Имя'})
    )
    phone = PhoneNumberField(
        region='RU',
        widget=RegionalPhoneNumberWidget(
            region='RU',
            attrs={'class': 'order__form_input',
                   'placeholder': '+7 (999) 000 00 00'
                   }
        ),
    )
    address = forms.CharField(
        max_length=65,
        widget=forms.widgets.TextInput(attrs={'class': 'order__form_input',
                                              'placeholder': 'Адрес доставки'})
    )
    delivery_time = forms.ChoiceField(
        choices=(
            ('1', 'Как можно скорее'),
            ('10', 'с 10:00 до 12:00'),
            ('12', 'с 12:00 до 14:00'),
            ('14', 'с 14:00 до 16:00'),
            ('16', 'с 16-00 до 18-00'),
            ('18', 'с 18-00 до 20-00'),
        ),
        widget=forms.widgets.RadioSelect(),
    )
