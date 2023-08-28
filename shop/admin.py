from django.contrib import admin
from django.utils.html import format_html

from .models import Event, Bouquet, Order, Consultation


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    readonly_fields = ['preview']
    fields = ['name', 'price', 'composition', 'description', 'size', 'events', 'photo', 'preview']
    
    def preview(self, bouquet):
        return format_html(
            '<img src={} height={}>',
            bouquet.photo.url,
            200
        )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'deliver', 'phone', 'address', 'status']
    list_filter = ['deliver', 'status']
    search_fields = ['phone', 'address']
    date_hierarchy = 'deliver'
    ordering = ['-deliver', 'status']
    raw_id_fields = ['bouquet']


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['datetime_created', 'client_name', 'phone']
    ordering = ['-datetime_created']
    list_filter = ['datetime_created']
    date_hierarchy = 'datetime_created'
