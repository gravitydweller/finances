# home/views.py
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from expenses.models import Expense
from incomes.models import Income
from pools.models import Pool, BalanceHistory
import json
from django.db.models.functions import Cast

from django.db.models import DecimalField
from datetime import date, timedelta
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.utils import timezone

from django.db.models import Sum, ExpressionWrapper, F, DecimalField

from core.utilities import *

import logging

from django.db.models import ExpressionWrapper, F, DecimalField
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from pools.models import Pool, BalanceHistory
from incomes.models import Income
from expenses.models import Expense
import json



def index(request):

    # Page from the theme 
    return render(request, 'pages/dashboard.html')



logger = logging.getLogger(__name__)

def create_balance_history_all_pools_data(pools, months_ago):
    balance_histories = {pool.name: [] for pool in pools}
    dates_set = set()
    some_months_ago = timezone.now() - timedelta(days=30 * months_ago)
    
    logger.debug(f"Calculating balance history from {some_months_ago} to {timezone.now()} for {months_ago} months ago")

    for pool in pools:
        balance_history = BalanceHistory.objects.filter(pool=pool, date__gte=some_months_ago, date__lte=timezone.now()).order_by('date')
        balance_history = balance_history.annotate(balance_float=ExpressionWrapper(F('balance'), output_field=DecimalField(max_digits=10, decimal_places=2)))
        
        for entry in balance_history:
            dates_set.add(entry.date)
            balance_histories[pool.name].append((entry.date.strftime('%Y-%m-%d'), float(entry.balance_float)))

    sorted_dates = sorted(dates_set)
    
    chart_data_time_balances = {
        'dates': [date.strftime('%Y-%m-%d') for date in sorted_dates],
        'balances': {}
    }
    
    for pool_name in balance_histories:
        pool_balances = []
        balance_history_dict = {date: balance for date, balance in balance_histories[pool_name]}
        last_balance = 0.0
        for date in sorted_dates:
            date_str = date.strftime('%Y-%m-%d')
            if date_str in balance_history_dict:
                last_balance = balance_history_dict[date_str]
            pool_balances.append(last_balance)
        chart_data_time_balances['balances'][pool_name] = pool_balances
    
    return chart_data_time_balances

def create_incomes_and_expenses_history_data(months_ago):
    some_months_ago = timezone.now() - timedelta(days=30 * months_ago)
    
    logger.debug(f"Calculating incomes and expenses from {some_months_ago} to {timezone.now()} for {months_ago} months ago")

    # Aggregate incomes by month for the specified time period, sorted by month
    incomes_by_month = Income.objects.filter(date__gte=some_months_ago) \
        .annotate(month=TruncMonth('date')) \
        .values('month') \
        .annotate(total_amount=Sum('amount')) \
        .order_by('month')

    # Aggregate expenses by month for the specified time period, sorted by month
    expenses_by_month = Expense.objects.filter(date__gte=some_months_ago) \
        .annotate(month=TruncMonth('date')) \
        .values('month') \
        .annotate(total_amount=Sum('amount')) \
        .order_by('month')

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

    return chart_data



def home_home(request):
    pools = list(Pool.objects.all())  # Ensure we are dealing with a list of pool instances
    print(pools)

    # Create incomes and expenses history data
    chart_data = create_incomes_and_expenses_history_data(HOME_MONTHLY_EXPENSES_DURATION)

    # Create balance history data for all pools
    chart_data_time_balances = create_balance_history_all_pools_data(pools, HOME_POOL_HISTORY_DURATION)


    return render(request, 'home/home_home.html', {
        'chart_data': json.dumps(chart_data),
        'chart_data_time_balances': json.dumps(chart_data_time_balances),
        'pools': pools,
        'HOME_MONTHLY_EXPENSES_DURATION': HOME_MONTHLY_EXPENSES_DURATION,
        'HOME_POOL_HISTORY_DURATION': HOME_POOL_HISTORY_DURATION,
    })