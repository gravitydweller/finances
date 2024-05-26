# expenses/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Expense
from .form import ExpenseForm

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

##################################################################################################
# EXPENSE_HOMEL VIEW
'''
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
'''

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

    # DATA FOR CHART - Expenses over time
    expenses = Expense.objects.all().order_by('date')
    dates = [expense.date.strftime('%Y-%m-%d') for expense in expenses]
    amounts = [expense.amount for expense in expenses]

    # DATA FOR CHART - Expenses by category in the last 6 months
    six_months_ago = datetime.now() - timedelta(days=6*30)
    expenses_last_6_months = Expense.objects.filter(date__gte=six_months_ago)
    categories = [expense.chategory.name for expense in expenses_last_6_months]
    category_totals = {}

    for expense in expenses_last_6_months:
        category_name = expense.chategory.name
        if category_name in category_totals:
            category_totals[category_name] += expense.amount
        else:
            category_totals[category_name] = expense.amount

    bar_chart_data = {
        'categories': list(category_totals.keys()),
        'amounts': list(category_totals.values()),
    }

    # Convert data to JSON format for use in JavaScript
    chart_data = {
        'dates': dates,
        'amounts': amounts,
    }

    return render(request, 'expense/expense_home.html', {
        'expenses': expenses_list,
        'form': form,
        'chart_data': json.dumps(chart_data),
        'bar_chart_data': json.dumps(bar_chart_data),
    })




##################################################################################################
# EXPENSE_DETAIL VIEW
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
