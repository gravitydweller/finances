# allocations/forms.py

from django import forms
from .models import IncomeAllocation


class IncomeAllocationForm(forms.ModelForm):
    class Meta:
        model = IncomeAllocation
        fields = ['income']