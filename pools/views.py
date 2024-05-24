# pools/views.py

from django.forms.models import model_to_dict
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pool, BalanceHistory
from .forms import PoolForm, PoolTransferForm
from django.db.models import DecimalField
from django.db.models.functions import Cast


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
# POOL HOME VIEW
def pool_home(request):
    # Get all pools
    pools = Pool.objects.all()

    # Extract pool names and current balances
    pool_names = [pool.name for pool in pools]
    current_balances = [pool.current_balance for pool in pools]

    # Prepare chart data
    chart_data = {
        'pool_names': pool_names,
        'current_balances': current_balances,
    }

    return render(request, 'pool/pool_home.html', {
        'chart_data': json.dumps(chart_data),
        'pools': pools,
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

    # Fetch balance history data related to the current pool
    balance_history = BalanceHistory.objects.filter(pool=pool).order_by('date')
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
