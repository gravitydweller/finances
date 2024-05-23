# history/admin.py

from django.contrib import admin
from .models import BalanceHistory

@admin.register(BalanceHistory)
class BalanceHistoryAdmin(admin.ModelAdmin):
    list_display = ('pool', 'date', 'balance')
    list_filter = ('pool', 'date')
    search_fields = ('pool__name',)
