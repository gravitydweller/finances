# history/models.py

from django.db import models
from pools.models import Pool

class BalanceHistory(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name='balance_history')
    date = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Balance for {self.pool.name} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}: {self.balance}"
