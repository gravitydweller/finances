# home/views.py
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from expenses.models import Expense
from incomes.models import Income
from pools.models import Pool
import json


# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/dashboard.html')



def home_home(request):

    # Aggregate incomes by month
    incomes_by_month = Income.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')[:12]

    # Aggregate expenses by month
    expenses_by_month = Expense.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')[:12]

    # Prepare data for the chart
    expense_months = [entry['month'].strftime('%Y-%m') for entry in expenses_by_month]
    income_months = [entry['month'].strftime('%Y-%m') for entry in incomes_by_month]

    # Combine expenses and incomes into a single list of months
    all_months = list(set(expense_months + income_months))
    all_months.sort()

    # Initialize total amounts for expenses and incomes for each month
    total_expenses = [0] * len(all_months)
    total_incomes = [0] * len(all_months)

    # Fill in total amounts for expenses by month
    for entry in expenses_by_month:
        index = all_months.index(entry['month'].strftime('%Y-%m'))
        total_expenses[index] = entry['total_amount']

    # Fill in total amounts for incomes by month
    for entry in incomes_by_month:
        index = all_months.index(entry['month'].strftime('%Y-%m'))
        total_incomes[index] = entry['total_amount']




    



    # Convert data to JSON format for use in JavaScript
    chart_data = {
        'months': all_months,
        'total_expenses': total_expenses,
        'total_incomes': total_incomes,
    }



    return render(request, 'home/home_home.html', {
        'chart_data': json.dumps(chart_data),
    })
