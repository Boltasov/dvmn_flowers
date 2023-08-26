from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.core.paginator import Paginator

from .models import Bouquet, Event, Consultation
from .forms import ConsultationFortm


def main_page(request):
    popular_bouquets = Bouquet.objects.all()\
        .annotate(count=Count('orders')).order_by('-count')[:3]
    return render(request, 'index.html', {
        'recomendations': popular_bouquets,
    })


def catalog(request):
    catalog_bouquets = Bouquet.objects.all()
    paginator = Paginator(catalog_bouquets, 6)
    number_pages = int(request.GET.get('page', 1))
    bouquets = []
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
    })


def show_card(request, id):
    bouquet = get_object_or_404(Bouquet, id=id)
    return render(request, 'card.html', {
        'bouquet': bouquet,
    })


def order(request):
    bouquet_id = request.GET.get('bouquet', 1)
    return render(request, 'order.html', {
        'id': bouquet_id,
    })


def pay_form(request, order_id):
    return render(request, 'order-step.html', {})


def quiz(request):
    events = Event.objects.all()
    return render(request, 'quiz.html', {'events': events})


def quiz_step(request, event_id):
    return render(request, 'quiz-step.html', {'event_id': event_id})


def result(request, event_id, price_level):
    match price_level:
        case 'low':
            best_bouquet = Event.objects.get(pk=event_id).bouquets.all().filter(price__lt=2000).first()
        case 'mid':
            best_bouquet = Event.objects.get(pk=event_id).bouquets.all().filter(price__gt=2000, price__lt=5000).first()
        case 'top':
            best_bouquet = Event.objects.get(pk=event_id).bouquets.all().filter(price__gt=5000).first()
        case _:
            best_bouquet = Event.objects.get(pk=event_id).bouquets.all().first()
    return render(request, 'result.html', {'bouquet': best_bouquet})


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
