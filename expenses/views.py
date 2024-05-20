# expenses/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .form import ExpenseForm

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def expense_home(request):
    # CREATE NEW EXPENSE
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('expense_home')
    else:
        form = ExpenseForm()

    # EXPENSE LIST
    expenses_list = Expense.objects.all().order_by('-date')

    # DATA FOR CHART
    expenses = Expense.objects.all().order_by('date')
    dates = [expense.date.strftime('%Y-%m-%d') for expense in expenses]
    amounts = [expense.amount for expense in expenses]

    # Convert data to JSON format for use in JavaScript
    chart_data = {
        'dates': dates,
        'amounts': amounts,
    }

    return render(request, 'expense/expense_home.html', {
        'expenses': expenses_list,
        'form': form,
        'chart_data': json.dumps(chart_data),
    })

def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    return render(request, 'expense/expense_detail.html', {'expense': expense})

def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('expense_home')
    else:
        form = ExpenseForm()
    return render(request, 'expense/expense_form.html', {'form': form})

def expense_update(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_home')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense/expense_form.html', {'form': form})

def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_home')
    return render(request, 'expense/expense_confirm_delete.html', {'expense': expense})
