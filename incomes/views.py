# incomes/views.py

from django.shortcuts import render, redirect
from .models import Income
from .forms import IncomeForm

def income_list(request):
    incomes = Income.objects.all()
    return render(request, 'income/income_list.html', {'incomes': incomes})

def income_detail(request, income_id):
    income = Income.objects.get(id=income_id)
    return render(request, 'income/income_detail.html', {'income': income})

def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'income/income_form.html', {'form': form})

def income_update(request, income_id):
    income = Income.objects.get(id=income_id)
    if request.method == 'POST':
        form = IncomeForm(request.POST, request.FILES, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'income/income_form.html', {'form': form})

def income_delete(request, income_id):
    income = Income.objects.get(id=income_id)
    if request.method == 'POST':
        income.delete()
        return redirect('income_list')
    return render(request, 'income/income_confirm_delete.html', {'income': income})

