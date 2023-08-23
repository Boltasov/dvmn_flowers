from django.shortcuts import render
from django.db.models import Count

from .models import Bouquet
from dvmn_flowers.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT


def main_page(request):
    popular_bouquets = Bouquet.objects.all()\
        .annotate(count=Count('orders')).order_by('-count')[:3]
    print(MEDIA_ROOT)
    print(MEDIA_URL)
    print(STATIC_ROOT)
    return render(request, 'index.html', {
        'recomendations': popular_bouquets,
        })
