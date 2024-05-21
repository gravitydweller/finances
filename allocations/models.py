# allocations/models.py

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from incomes.models import Income
from pools.models import Pool

class IncomeAllocation(models.Model):
    income = models.OneToOneField(Income, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.income}"



# Define a function to allocate income to pools
def allocate_income_to_pools(income_allocation_instance):
    income_instance = income_allocation_instance.income
    income_amount = income_instance.amount
    income_amount = float(income_amount)
    pools = Pool.objects.all()

    # Calculate total fixed amount for all pools
    total_fixed_amount = sum(pool.allocated_fixed for pool in pools)

    # Ensure allocation_amount_fixed is a float
    allocation_amount_fixed = min(total_fixed_amount, income_amount)

    # Calculate allocation amount for proportional distribution
    allocation_amount_proportion = income_amount - allocation_amount_fixed

    # Distribute remaining amount proportionally to pools based on their percentages
    for pool in pools:
        pool_allocation_proportion = (pool.allocated_procentage / 100) * allocation_amount_proportion
        pool_allocation_total = pool_allocation_proportion + pool.allocated_fixed
        pool.current_balance += pool_allocation_total
        pool.save()

        # Update balance history
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


@receiver(post_save, sender=IncomeAllocation)
def allocate_income(sender, instance, created, **kwargs):
    if created:
        allocate_income_to_pools(instance)

        # Change status of Income.allocated from False to True
        income_instance = instance.income
        income_instance.allocated = True
        income_instance.save()
