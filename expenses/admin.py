# expenses/admin.py

from django.contrib import admin
from. models import Expense, ExpenseTag, ExpenseCategory
admin.site.register(Expense)
admin.site.register(ExpenseTag)
admin.site.register(ExpenseCategory)
