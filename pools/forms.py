# pools/forms.py

from django import forms
from .models import Pool, PoolTransfer


class PoolForm(forms.ModelForm):
    class Meta:
        model = Pool
        fields = ['name', 'type', 'current_balance', 'allocated_procentage', 'allocated_fixed']

class PoolTransferForm(forms.ModelForm):
    class Meta:
        model = PoolTransfer
        fields = ['date', 'source_pool', 'destination_pool', 'amount']

class PoolUpdateForm(forms.ModelForm):
    class Meta:
        model = Pool
        fields = ['allocated_procentage', 'allocated_fixed']