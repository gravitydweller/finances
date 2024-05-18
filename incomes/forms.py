# incomes/forms.py

from django import forms
from .models import Income

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['employer', 'tag', 'amount', 'description', 'date', 'attachment', 'allocated']
