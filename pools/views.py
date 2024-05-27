# pools/views.py

from django.forms.models import model_to_dict
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pool, BalanceHistory
from .forms import PoolForm, PoolTransferForm
from django.db.models import DecimalField
from django.db.models.functions import Cast


from datetime import date, timedelta
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.utils import timezone


MONTHS_AGO = 9

def pool_transfer_create(request):
    source_pools = Pool.objects.all()
    destination_pools = Pool.objects.all()

    if request.method == 'POST':
        form = PoolTransferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pool_home')
    else:
        form = PoolTransferForm()
    
    return render(request, 'pool/pool_transfer.html', {
        'form': form,
        'source_pools': source_pools,
        'destination_pools': destination_pools,
    })


def pool_update(request, pool_id):
    pool = get_object_or_404(Pool, id=pool_id)
    if request.method == 'POST':
        form = PoolForm(request.POST, instance=pool)
        if form.is_valid():
            form.save()
            return redirect('pool_list')
    else:
        form = PoolForm(instance=pool)
    return render(request, 'pool/pool_form.html', {'form': form})




##################################################################################################
# INDIVIDUAL POOL VIEW
def pool_detail(request, pool_id):
    pool = get_object_or_404(Pool, id=pool_id)
    if request.method == 'POST':
        form = PoolForm(request.POST, instance=pool)
        if form.is_valid():
            form.save()
    else:
        form = PoolForm(instance=pool)

    # Calculate the date some months ago from the current date
        some_months_ago = timezone.now() - timedelta(days=30 * MONTHS_AGO)

    # Filter the balance history records for the some months ago
    balance_history = BalanceHistory.objects.filter(pool=pool, date__gte=some_months_ago, date__lte=timezone.now()).order_by('date')
    # Convert Decimal objects to float
    balance_history = balance_history.annotate(balance_float=Cast('balance', DecimalField(max_digits=10, decimal_places=2)))
    dates = [entry.date.strftime('%Y-%m-%d') for entry in balance_history]
    # Convert balance_float to float
    balances = [float(entry.balance_float) for entry in balance_history]

    chart_data = {
        'dates': dates,
        'balances': balances,
    }

    return render(request, 'pool/pool_detail.html', {
        'pool': pool,
        'form': form,
        'chart_data': json.dumps(chart_data),
    })


##################################################################################################
# POOL HOME VIEW
def pool_home(request):
    # ALL POOL BALANCES HISTORIES ################################################################
    pools = Pool.objects.all()

    # Extract pool names and current balances
    pool_names = [pool.name for pool in pools]
    current_balances = [float(pool.current_balance) for pool in pools]

    pools = Pool.objects.all()

    # Extract pool names and current balances
    pool_names = [pool.name for pool in pools]
    current_balances = [float(pool.current_balance) for pool in pools]

    # Prepare data for the chart of current balances
    chart_data_current_balances = {
        'pool_names': pool_names,
        'current_balances': current_balances,
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
    return render(request, 'pool/pool_home.html', {
        'chart_data_current_balances': json.dumps(chart_data_current_balances),
        'chart_data_reserve_time_balances': json.dumps(chart_data_reserve_time_balances),
        'chart_data_cost_time_balances': json.dumps(chart_data_cost_time_balances),
        'chart_data_investment_time_balances': json.dumps(chart_data_investment_time_balances),
        'pools': pools,
        'some_months_ago': MONTHS_AGO,
    })

