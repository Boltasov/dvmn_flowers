from django.contrib import admin

from .models import Event, Bouquet, Order, Consultation


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    pass
