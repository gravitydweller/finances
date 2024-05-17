# pools/admin.py

from django.contrib import admin
from. models import Pool, PoolTransfer

admin.site.register(Pool)
admin.site.register(PoolTransfer)
