# expenses/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Expense, ExpenseTag, ExpenseCategory, UTILITY_CHOICES
from .form import ExpenseForm

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from core.utilities import *


def handle_expense_form_submission(request):
    form = ExpenseForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return True
    return False


def get_expenses_over_time_chart_data():
    expenses = Expense.objects.all()  # Adjust the filter if necessary
    dates = [expense.date.strftime('%Y-%m-%d') for expense in expenses]  # Ensure dates are strings
    amounts = [expense.amount for expense in expenses]
    return {'dates': dates, 'amounts': amounts}

def get_expenses_by_tag_chart_data():
    tags = ExpenseTag.objects.all()
    tag_names = []
    tag_amounts = []

    for tag in tags:
        expenses_for_tag = Expense.objects.filter(tag=tag)
        total_amount_for_tag = sum(expense.amount for expense in expenses_for_tag)
        if total_amount_for_tag > 0:
            tag_names.append(tag.name)  # Ensure the tag name is a string
            tag_amounts.append(total_amount_for_tag)

    if tag_names:
        return {'tags': tag_names, 'amounts': tag_amounts}
    return None

def get_expenses_by_category_chart_data():
    expenses_last_some_months = Expense.objects.all()

    category_totals = {}
    for expense in expenses_last_some_months:
        category_name = str(expense.category)  # Ensure the category is a string
        if category_name in category_totals:
            category_totals[category_name] += expense.amount
        else:
            category_totals[category_name] = expense.amount

    return {'categories': list(category_totals.keys()), 'amounts': list(category_totals.values())}


##################################################################################################
# EXPENSE_HOMEL VIEW
def expense_home(request):
    if request.method == 'POST':
        if handle_expense_form_submission(request):
            return redirect('expense_home')

    form = ExpenseForm()
    expenses_list = Expense.objects.all().order_by('-date')
    all_chart_data = get_expenses_over_time_chart_data()
    categories_chart_data = get_expenses_by_category_chart_data()
    tag_chart_data = get_expenses_by_tag_chart_data()

    context = {
        'expenses': expenses_list,
        'form': form,
        'all_chart_data': json.dumps(all_chart_data),
        'categories_chart_data': json.dumps(categories_chart_data),
        'tag_chart_data': json.dumps(tag_chart_data),
        #'some_months_ago': EXPENSE_HOME_DURATION,
    }

    return render(request, 'expense/expense_home.html', context)






##################################################################################################
# EXPENSE DETAIL VIEW
def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    return render(request, 'expense/expense_detail.html', {'expense': expense})

##################################################################################################
# EXPENSE CREATE VIEW
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('expense_home')
    else:
        form = ExpenseForm()

    context = {
        'form': form,
        'UTILITY_CHOICES': UTILITY_CHOICES,
    }

    return render(request, 'expense/expense_form.html', context)



##################################################################################################
# EXPENSE UPDATE VIEW
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

##################################################################################################
# EXPENSE DELETE VIEW
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_home')
    return render(request, 'expense/expense_confirm_delete.html', {'expense': expense})

