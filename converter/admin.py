# converter/admin.py
from django.contrib import admin
from .models import Conversion

@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ('timestamp','user','from_currency','to_currency','from_amount','to_amount','raw_rate')
    list_filter = ('from_currency','to_currency')
    search_fields = ('user__username','from_currency','to_currency')
