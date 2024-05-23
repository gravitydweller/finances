# history/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BalanceHistory
from allocations.models import IncomeAllocation
from expenses.models import Expense
from pools.models import Pool, PoolTransfer

@receiver(post_save, sender=IncomeAllocation)
@receiver(post_save, sender=Expense)
@receiver(post_save, sender=PoolTransfer)
def log_balance_change(sender, instance, created, **kwargs):
    if created:
        # Determine the pool and amount
        if isinstance(instance, IncomeAllocation):
            pool = instance.income.pool
            amount = instance.income.amount
        elif isinstance(instance, Expense):
            pool = instance.tag.source_pool
            amount = -instance.amount
        elif isinstance(instance, PoolTransfer):
            pool = instance.source_pool
            amount = -instance.amount
        else:
            return

        # Update the pool's current balance
        pool.current_balance += amount
        pool.save()

        # Create a new balance history entry
        BalanceHistory.objects.create(
            pool=pool,
            balance=pool.current_balance,
        )
