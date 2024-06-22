# loans/forms.py

from django import forms
from .models import Loan

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['name', 'amount', 'duration_months', 'start_date', 'image', 'source_pool']

        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'source_pool': forms.Select(attrs={'class': 'form-control'}),
        }
