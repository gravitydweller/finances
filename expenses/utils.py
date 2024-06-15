# expenses/utils.py

from .models import Expense, ExpenseTag, ExpenseCategory, UTILITY_CHOICES
from .form import ExpenseForm
from core.utils import hex_to_rgba
from django.shortcuts import render, redirect

################################################################################################
# All expenses barchart  (function)
################################################################################################
def AllExpensesBarChart():
    expenses = Expense.objects.all()  # Adjust the filter if necessary
    dates = [expense.date.strftime('%Y-%m-%d') for expense in expenses]  # Ensure dates are strings
    amounts = [expense.amount for expense in expenses]
    colors = [expense.tag.color for expense in expenses if expense.tag]
    diluted_colors = [hex_to_rgba(color) for color in colors]

    return {
        'dates': dates,
        'amounts': amounts,
        'colors': colors,
        'diluted_colors': diluted_colors
        }

def EXPENSES_BY_TAG_PLOT():
    tags = ExpenseTag.objects.all()
    tag_names = []
    tag_amounts = []
    tag_colors = []
    diluted_colors = []

    for tag in tags:
        expenses_for_tag = Expense.objects.filter(tag=tag)
        total_amount_for_tag = sum(expense.amount for expense in expenses_for_tag)
        if total_amount_for_tag > 0:
            tag_names.append(tag.name)  # Ensure the tag name is a string
            tag_amounts.append(total_amount_for_tag)
            tag_colors.append(tag.color)
            diluted_colors.append(hex_to_rgba(tag.color))  # Default alpha value used for dilution


    return {
        'tags': tag_names,
        'amounts': tag_amounts,
        'colors': tag_colors,
        'diluted_colors': diluted_colors
        }


def EXPENSES_BY_CATEGORY_PLOT():
    expenses_last_some_months = Expense.objects.all()

    category_totals = {}
    for expense in expenses_last_some_months:
        category_name = str(expense.category)  # Ensure the category is a string
        if category_name in category_totals:
            category_totals[category_name] += expense.amount
        else:
            category_totals[category_name] = expense.amount

    return {'categories': list(category_totals.keys()), 'amounts': list(category_totals.values())}


def handle_expense_form_submission(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('expense_home')  # Redirect to the expense home page after successful form submission
    else:
        form = ExpenseForm()

    context = {
        'form': form,
    }

    return render(request, 'expense/expense_form.html', context)