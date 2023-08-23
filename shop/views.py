from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Bouquet
from dvmn_flowers.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT


def main_page(request):
    popular_bouquets = Bouquet.objects.all()\
        .annotate(count=Count('orders')).order_by('-count')[:3]
    return render(request, 'index.html', {
        'recomendations': popular_bouquets,
    })


def division_rows(page, item_per_row):
    for i in range(0, len(page), item_per_row):
        yield page[i : i + 1]


def catalog(request):
    catalog_bouquets = Bouquet.objects.all()
    paginator = Paginator(catalog_bouquets, 6)
    number_pages = request.GET.get('page', 1)
    bouquets = paginator.page(1)
    if number_pages > 1:
        for page in range(2, number_pages):
            bouquets = bouquets.union(paginator.page(page))
    catalog = list(division_rows(list(bouquets), 3))
    print(bouquets)
    print(catalog)
    return render(request, 'catalog.html', {
        'catalog': catalog,
    })