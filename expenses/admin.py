# expenses/admin.py

from django.contrib import admin
from. models import Expense, ExpenseTag, ExpenseChategory
admin.site.register(Expense)
admin.site.register(ExpenseTag)
admin.site.register(ExpenseChategory)
