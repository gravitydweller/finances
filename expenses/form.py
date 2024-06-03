# expenses/forms.py

from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['tag', 'date', 'bill_number', 'amount', 'description', 'attachment', 'category']
        widgets = {
            'tag': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tag'].initial = 'food'  # Set the default tag here
        self.fields['category'].initial = 'normal expense'  # Set the default category here