import datetime
import os
import uuid

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db.models import Count
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils import timezone

from .models import Bouquet, Event, Consultation, Order
from .forms import ConsultationFortm, OrderForm

from dotenv import load_dotenv
from yookassa import Configuration, Payment


def main_page(request):
    popular_bouquets = Bouquet.objects.all()\
        .annotate(count=Count('orders')).order_by('-count')[:3]
    form = ConsultationFortm()
    return render(request, 'index.html', {
        'recomendations': popular_bouquets,
        'form': form,
    })


def catalog(request):
    catalog_bouquets = Bouquet.objects.all()
    paginator = Paginator(catalog_bouquets, 6)
    number_pages = int(request.GET.get('page', 1))
    bouquets = []
    form = ConsultationFortm()
    for page in range(1, number_pages + 1):
        print('We are here')
        bouquets = bouquets + list(paginator.page(page))
    chunks = [bouquets[i:i + 3] for i in range(0, len(bouquets), 3)]
    next_page = number_pages + 1
    button = True
    if paginator.num_pages <= number_pages:
        button = False
    return render(request, 'catalog.html', {
        'catalog': chunks,
        'next_page': next_page,
        'button': button,
        'form': form,
    })


def show_card(request, id):
    bouquet = get_object_or_404(Bouquet, id=id)
    form = ConsultationFortm()
    return render(request, 'card.html', {
        'bouquet': bouquet,
        'form': form,
    })


def order(request):
    bouquet_id = request.GET.get('bouquet', 1)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_data = form.cleaned_data
            print(order_data)
            now = timezone.now()
            if order_data['delivery_time'] == '1':
                if now.time() < datetime.time(hour=20):
                    time = datetime.time(hour=10) if now.time() <= \
                        datetime.time(hour=8) else now + \
                        datetime.timedelta(hours=2)
                    delivery_time = datetime.datetime.combine(now.date(), time)
                else:
                    tomorrow = (now + datetime.timedelta(days=1)).date()
                    time = datetime.time(hour=10)
                    delivery_time = datetime.datetime.combine(tomorrow, time)
            else:
                time = datetime.time(hour=int(order_data['delivery_time']))
                if now.time() > time:
                    tomorrow = (now + datetime.timedelta(days=1)).date()
                    delivery_time = datetime.datetime.combine(tomorrow, time)
                else:
                    delivery_time = datetime.datetime.combine(now.date(), time)

            name = order_data['name']
            phone = order_data['phone']
            address = order_data['address']
            bouquet = Bouquet.objects.get(id=bouquet_id)
            new_order = Order(
                client_name=name,
                phone=phone,
                address=address,
                deliver=delivery_time,
                status=Order.Status.CREATED,
            )
            new_order.save()
            new_order.bouquet.set([bouquet])

            load_dotenv()
            account_id = os.getenv('ACCOUNT_ID')
            secret_key = os.getenv('SECRET_KEY')
            Configuration.configure(account_id, secret_key)

            idempotence_key = str(uuid.uuid4())
            return_url = request.build_absolute_uri(reverse('shop:pay_form', args=(new_order.id,)))
            payment = Payment.create({
                "amount": {
                    "value": "100.00",
                    "currency": "RUB"
                },
                "payment_method_data": {
                    "type": "bank_card"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": return_url
                },
                "description": "Донат на митапе"
            }, idempotence_key)

            confirmation_url = payment.confirmation.confirmation_url

            return HttpResponseRedirect(confirmation_url)
            #return HttpResponseRedirect(reverse('shop:pay_form',
            #                                    args=(new_order.id,)))

    form = OrderForm()
    return render(request, 'order.html', {
        'id': bouquet_id,
        'form': form,
    })


def pay_form(request, order_id):
    order = Order.objects.get(id=order_id)
    order.paid = True
    order.save()
    return main_page(request)
    #return render(request, 'order-step.html', {})


def quiz(request):
    events = Event.objects.all()
    return render(request, 'quiz.html', {'events': events})


def quiz_step(request, event_id):
    return render(request, 'quiz-step.html', {'event_id': event_id})


def result(request, event_id, price_level):
    form = ConsultationFortm()
    match price_level:
        case 'low':
            best_bouquet = Event.objects.get(pk=event_id).bouquets.all()\
                .filter(price__lt=2000).first()
        case 'mid':
            best_bouquet = Event.objects.get(pk=event_id).bouquets.all()\
                .filter(price__gt=2000, price__lt=5000).first()
        case 'top':
            best_bouquet = Event.objects.get(pk=event_id).bouquets.all()\
                .filter(price__gt=5000).first()
        case _:
            best_bouquet = Event.objects.get(pk=event_id).bouquets.all()\
                .first()
    return render(request, 'result.html', {'bouquet': best_bouquet,
                                           'form': form})


def consultation(request):
    mark = False
    if request.method == 'POST':
        form = ConsultationFortm(request.POST)
        if form.is_valid():
            client_data = form.cleaned_data

            appointment = Consultation(
                client_name=client_data['name'],
                phone=client_data['phone']
            )
            appointment.save()
            mark = True
    else:
        form = ConsultationFortm()
    return render(request, 'consultation.html', {
        'form': form,
        'mark': mark,
    })


def confidentcialnost(request):
    return render(request, 'confidentcialnost.html', {})
