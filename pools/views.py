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

from core.utilities import *


def create_balance_history_data_for_(pools, months_ago):
    balance_histories = {pool.name: [] for pool in pools}
    dates_set = set()
    some_months_ago = timezone.now() - timedelta(days=30 * months_ago)
    
    for pool in pools:
        balance_history = BalanceHistory.objects.filter(pool=pool, date__gte=some_months_ago, date__lte=timezone.now()).order_by('date')
        balance_history = balance_history.annotate(balance_float=Cast('balance', DecimalField(max_digits=10, decimal_places=2)))
        
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


##################################################################################################
# POOL HOME VIEW
def pool_home(request):
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
    chart_data_reserve_time_balances = create_balance_history_data_for_(reserve_pools, POOL_HOME_DURATION)

    # COST POOL BALANCES HISTORIES ################################################################
    cost_pools = pools.filter(type='cost')
    chart_data_cost_time_balances = create_balance_history_data_for_(cost_pools, POOL_HOME_DURATION)

    # INVESTMENT POOL BALANCES HISTORIES ################################################################
    investment_pools = pools.filter(type='investment')
    chart_data_investment_time_balances = create_balance_history_data_for_(investment_pools, POOL_HOME_DURATION)

    # RENDER DATA
    return render(request, 'pool/pool_home.html', {
        'chart_data_current_balances': json.dumps(chart_data_current_balances),
        'chart_data_reserve_time_balances': json.dumps(chart_data_reserve_time_balances),
        'chart_data_cost_time_balances': json.dumps(chart_data_cost_time_balances),
        'chart_data_investment_time_balances': json.dumps(chart_data_investment_time_balances),
        'pools': pools,
        'some_months_ago': POOL_HOME_DURATION,
    })


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
    some_months_ago = timezone.now() - timedelta(days=30 * POOL_HOME_DURATION)

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
# POOL TRANSFER VIEW
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


##################################################################################################
# POOL UPDATE VIEW
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