from django.contrib import admin
from .models import Mechanic, ServiceRequest


@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'location', 'rating', 'is_open')
    search_fields = ('name', 'location', 'phone')
    list_filter = ('is_open', 'rating')


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'customer_phone',
        'vehicle_number',
        'service',
        'mechanic',
        'status',
        'created_at',
    )
    search_fields = (
        'customer_name',
        'customer_phone',
        'vehicle_number',
        'service',
    )
    list_filter = ('status', 'created_at')