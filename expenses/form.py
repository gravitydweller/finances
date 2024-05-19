# expenses/forms.py

from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['tag', 'date' ,'bill_number','amount', 'description', 'attachment', 'chategory']