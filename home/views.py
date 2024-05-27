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



MONTHS_AGO = 9
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



    pools = Pool.objects.all()

    



    # Convert data to JSON format for use in JavaScript
    chart_data = {
        'months': all_months,
        'total_expenses': total_expenses,
        'total_incomes': total_incomes,
    }



    # RESERVE POOL BALANCES HISTORIES ################################################################
    reserve_pools = pools.filter(type='reserve')
    reserve_pool_names = [reserve_pool.name for reserve_pool in reserve_pools]

    reserve_balance_histories = {pool.name: [] for pool in reserve_pools}
    reserve_dates_set = set()

    # Fetch balance history data for reserve pools
    for pool in reserve_pools:
        some_months_ago = timezone.now() - timedelta(days=30 * MONTHS_AGO)
        balance_history = BalanceHistory.objects.filter(pool=pool, date__gte=some_months_ago, date__lte=timezone.now()).order_by('date')
        balance_history = balance_history.annotate(balance_float=Cast('balance', DecimalField(max_digits=10, decimal_places=2)))
        for entry in balance_history:
            reserve_dates_set.add(entry.date)
            reserve_balance_histories[pool.name].append((entry.date.strftime('%Y-%m-%d'), float(entry.balance_float)))

    reserve_sorted_dates = sorted(reserve_dates_set)  

    chart_data_reserve_time_balances = {
        'dates': [date.strftime('%Y-%m-%d') for date in reserve_sorted_dates],
        'balances': {}
    }

    for pool_name in reserve_pool_names:
        pool_balances = []
        balance_history_dict = {date: balance for date, balance in reserve_balance_histories[pool_name]}
        last_balance = 0.0
        for date in reserve_sorted_dates:
            date_str = date.strftime('%Y-%m-%d')
            if date_str in balance_history_dict:
                last_balance = balance_history_dict[date_str]
            pool_balances.append(last_balance)
        chart_data_reserve_time_balances['balances'][pool_name] = pool_balances


    # COST POOL BALANCES HISTORIES ################################################################
    cost_pools = pools.filter(type='cost')
    cost_pool_names = [cost_pool.name for cost_pool in cost_pools]

    cost_balance_histories = {pool.name: [] for pool in cost_pools}
    cost_dates_set = set()

    # Fetch balance history data for cost pools
    for pool in cost_pools:
        some_months_ago = timezone.now() - timedelta(days=30 * MONTHS_AGO)
        balance_history = BalanceHistory.objects.filter(pool=pool, date__gte=some_months_ago, date__lte=timezone.now()).order_by('date')
        balance_history = balance_history.annotate(balance_float=Cast('balance', DecimalField(max_digits=10, decimal_places=2)))
        for entry in balance_history:
            cost_dates_set.add(entry.date)
            cost_balance_histories[pool.name].append((entry.date.strftime('%Y-%m-%d'), float(entry.balance_float)))

    cost_sorted_dates = sorted(cost_dates_set)  

    chart_data_cost_time_balances = {
        'dates': [date.strftime('%Y-%m-%d') for date in cost_sorted_dates],
        'balances': {}
    }

    for pool_name in cost_pool_names:
        pool_balances = []
        balance_history_dict = {date: balance for date, balance in cost_balance_histories[pool_name]}
        last_balance = 0.0
        for date in cost_sorted_dates:
            date_str = date.strftime('%Y-%m-%d')
            if date_str in balance_history_dict:
                last_balance = balance_history_dict[date_str]
            pool_balances.append(last_balance)
        chart_data_cost_time_balances['balances'][pool_name] = pool_balances


    # INVESTMENT POOL BALANCES HISTORIES ################################################################
    investment_pools = pools.filter(type='investment')
    investment_pool_names = [investment_pool.name for investment_pool in investment_pools]

    investment_balance_histories = {pool.name: [] for pool in investment_pools}
    investment_dates_set = set()

    # Fetch balance history data for investment pools
    for pool in investment_pools:
        some_months_ago = timezone.now() - timedelta(days=30 * MONTHS_AGO)
        balance_history = BalanceHistory.objects.filter(pool=pool, date__gte=some_months_ago, date__lte=timezone.now()).order_by('date')
        balance_history = balance_history.annotate(balance_float=Cast('balance', DecimalField(max_digits=10, decimal_places=2)))
        for entry in balance_history:
            investment_dates_set.add(entry.date)
            investment_balance_histories[pool.name].append((entry.date.strftime('%Y-%m-%d'), float(entry.balance_float)))

    investment_sorted_dates = sorted(investment_dates_set)  

    chart_data_investment_time_balances = {
        'dates': [date.strftime('%Y-%m-%d') for date in investment_sorted_dates],
        'balances': {}
    }

    for pool_name in investment_pool_names:
        pool_balances = []
        balance_history_dict = {date: balance for date, balance in investment_balance_histories[pool_name]}
        last_balance = 0.0
        for date in investment_sorted_dates:
            date_str = date.strftime('%Y-%m-%d')
            if date_str in balance_history_dict:
                last_balance = balance_history_dict[date_str]
            pool_balances.append(last_balance)
        chart_data_investment_time_balances['balances'][pool_name] = pool_balances

    # RENDER DATA
    return render(request, 'home/home_home.html', {
        'chart_data': json.dumps(chart_data),
        'chart_data_reserve_time_balances': json.dumps(chart_data_reserve_time_balances),
        'chart_data_cost_time_balances': json.dumps(chart_data_cost_time_balances),
        'chart_data_investment_time_balances': json.dumps(chart_data_investment_time_balances),
        'pools': pools,
        'some_months_ago': MONTHS_AGO,
    })
