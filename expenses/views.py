# expenses/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from .utils import handle_expense_form_submission, AllExpensesBarChart, EXPENSES_BY_TAG_PLOT, EXPENSES_BY_CATEGORY_PLOT, Expense, ExpenseForm, ExpenseTag, ExpenseCategory, UTILITY_CHOICES


##################################################################################################
# EXPENSE_HOMEL VIEW
def expense_home(request):
    if request.method == 'POST':
        if handle_expense_form_submission(request):
            return redirect('expense_home')

    form = ExpenseForm()
    expenses_list = Expense.objects.all().order_by('-date')
    all_data = AllExpensesBarChart()
    categories_data = EXPENSES_BY_CATEGORY_PLOT()
    tag_data = EXPENSES_BY_TAG_PLOT()

    context = {
        'expenses': expenses_list,
        'form': form,
        'all_data': json.dumps(all_data),
        'categories_data': json.dumps(categories_data),
        'tag_data': json.dumps(tag_data),
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

    # Fetch all ExpenseTags containing the word "loan" in their name
    loan_tags = list(ExpenseTag.objects.filter(name__icontains="loan"))
    
    # Prepare LOAN_CHOICES in the format [('tag_id', 'Tag Name')]
    LOAN_CHOICES = [(tag.name, tag.name) for tag in loan_tags]

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
        'LOAN_CHOICES': LOAN_CHOICES,
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

