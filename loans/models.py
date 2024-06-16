# loans/models.py

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from expenses.models import Expense, ExpenseTag, ExpenseCategory
from pools.models import Pool
from datetime import timedelta

class Loan(models.Model):
    name = models.CharField(max_length=200)
    amount = models.FloatField()
    duration_months = models.IntegerField()
    start_date = models.DateTimeField()
    image = models.ImageField(upload_to='loans/images/', blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    source_pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class LoanExpense(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='expenses')
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='loan_expenses')

    def __str__(self):
        return f"Loan: {self.loan.name} - Expense: {self.expense.description}"


# Function to calculate end_date before saving Loan object
@receiver(pre_save, sender=Loan)
def calculate_end_date(sender, instance, **kwargs):
    if not instance.end_date:  # If end_date is not set
        # Calculate end_date based on start_date and duration_months
        instance.end_date = instance.start_date + timedelta(days=30 * instance.duration_months)




@receiver(post_save, sender=Loan)
def create_expense_tag_for_loan(sender, instance, created, **kwargs):
    if created:
        # Assuming you have a default pool or you can set one dynamically
        default_pool = Pool.objects.first()  # Change this as per your logic
        ExpenseTag.objects.create(name=f"{instance.name} loan", source_pool=instance.source_pool)

# Connect the signal to the create_expense_tag_for_loan function
post_save.connect(create_expense_tag_for_loan, sender=Loan)
