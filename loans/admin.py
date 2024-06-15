# loans/admin.py

from django.contrib import admin
from .models import Loan, LoanExpense



admin.site.register(Loan)
admin.site.register(LoanExpense)
