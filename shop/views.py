from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.core.paginator import Paginator

from .models import Bouquet


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