# incomes/views.py

from django.shortcuts import render, redirect
from .models import Income
from .forms import IncomeForm

import json
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def income_detail(request, income_id):
    income = Income.objects.get(id=income_id)
    return render(request, 'income/income_detail.html', {'income': income})

def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('income_home')
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


##################################################################################################

def income_home(request):
    # CREATE NEW INCOME
    if request.method == 'POST':
        form = IncomeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('income_home')
    else:
        form = IncomeForm()

    # INCOMES LIST
    incomes = Income.objects.all()

    # DATA FOR CHART
    incomes = Income.objects.all().order_by('date')
    dates = [income.date.strftime('%Y-%m-%d') for income in incomes]
    amounts = [income.amount for income in incomes]

    # Convert data to JSON format for use in JavaScript
    chart_data = {
        'dates': dates,
        'amounts': amounts,
    }

    return render(request, 'income/income_home.html', {
        'incomes': incomes,
        'form': form,
        'chart_data': json.dumps(chart_data),
    })
