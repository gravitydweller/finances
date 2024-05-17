# expenses/admin.py

from django.contrib import admin
from. models import Expense, ExpenseTag

admin.site.register(Expense)
admin.site.register(ExpenseTag)
