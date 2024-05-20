# pools/admin.py

from django.contrib import admin
from. models import Pool, PoolTransfer, BalanceHistory


admin.site.register(Pool)
admin.site.register(PoolTransfer)
admin.site.register(BalanceHistory)