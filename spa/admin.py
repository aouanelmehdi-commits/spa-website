from django.contrib import admin
from .models import Booking, ContactMessage

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['first_name', 'last_name', 'service', 'date', 'time', 'status', 'created_at']
    list_filter   = ['status', 'service']
    search_fields = ['first_name', 'last_name', 'email']
    list_editable = ['status']

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display  = ['first_name', 'last_name', 'email', 'phone', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']