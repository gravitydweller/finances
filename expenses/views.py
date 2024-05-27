# expenses/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Expense, ExpenseTag
from .form import ExpenseForm

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

MONTHS_AGO = 3

##################################################################################################
# EXPENSE_HOMEL VIEW

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

    # Convert data to JSON format for use in JavaScript
    all_chart_data = {
        'dates': dates,
        'amounts': amounts,
    }

    # DATA FOR CHART - Expenses by category in the last X months
    some_months_ago = datetime.now() - timedelta(days=MONTHS_AGO*30)
    expenses_last_some_months = Expense.objects.filter(date__gte=some_months_ago)
    
    category_totals = {}

    for expense in expenses_last_some_months:
        category_name = expense.chategory.name
        if category_name in category_totals:
            category_totals[category_name] += expense.amount
        else:
            category_totals[category_name] = expense.amount

    categories_chart_data = {
        'categories': list(category_totals.keys()),
        'amounts': list(category_totals.values()),
    }

    # DATA FOR CHART - Expenses by category in the last X months
    tags = ExpenseTag.objects.all()

   

    
    return render(request, 'expense/expense_home.html', {
        'expenses': expenses_list,
        'form': form,
        'all_chart_data': json.dumps(all_chart_data),
        'categories_chart_data': json.dumps(categories_chart_data),
        #'tag_chart_data': json.dumps(tag_chart_data),
        'some_months_ago': MONTHS_AGO,
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

