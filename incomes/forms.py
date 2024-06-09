# incomes/forms.py

from django import forms
from .models import Income
from django.utils import timezone

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['employer', 'tag', 'amount', 'description', 'date', 'attachment', 'allocated']

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now()