# expenses/models.py

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pools.models import Pool, BalanceHistory

class ExpenseTag(models.Model):
    name = models.CharField(max_length=50)
    source_pool = models.ForeignKey(Pool, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class ExpenseChategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Expense(models.Model):
    tag = models.ForeignKey(ExpenseTag, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    bill_number = models.CharField(max_length=200, default='', blank=True, null=True)
    amount = models.FloatField()
    description = models.CharField(max_length=200, default='', blank=True, null=True)
    attachment = models.FileField(upload_to='expenses/attachments/', blank=True, null=True)
    chategory = models.ForeignKey(ExpenseChategory, default='', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.tag} - {self.date} - {self.description}"


@receiver(post_save, sender=Expense)
def update_pool_balance(sender, instance, created, **kwargs):
    """
    Automatically update the source pool balance when an expense is created.
    """
    if created:  # Only update balance if the expense is newly created
        source_pool = instance.tag.source_pool
        source_pool.current_balance -= instance.amount
        source_pool.save()

        # Create balance history with the date of the expense
        BalanceHistory.objects.create(pool=source_pool, balance=source_pool.current_balance, date=instance.date)

# Connect the signal to the update_pool_balance function
post_save.connect(update_pool_balance, sender=Expense)



