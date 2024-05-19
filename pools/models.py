# pools/models.py

from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Pool(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    current_balance = models.FloatField()
    allocated_procentage = models.FloatField()
    allocated_fixed = models.FloatField()

    def __str__(self):
        return f"{self.name}"





class BalanceHistory(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    balance = models.FloatField()

    def __str__(self):
        return f"{self.pool.name} - {self.date}"







class PoolTransfer(models.Model):
    date = models.DateField()
    source_pool = models.ForeignKey(Pool, related_name='transfers_from', on_delete=models.CASCADE)
    destination_pool = models.ForeignKey(Pool, related_name='transfers_to', on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.amount} from {self.source_pool} to {self.destination_pool} on {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update source pool balance
        self.source_pool.current_balance -= self.amount
        self.source_pool.save()
        # Update destination pool balance
        self.destination_pool.current_balance += self.amount
        self.destination_pool.save()