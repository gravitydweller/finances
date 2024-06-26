# pools/views.py

from django.forms.models import model_to_dict
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pool, BalanceHistory
from .forms import PoolForm, PoolTransferForm
from .utils import CurrentBalancesBarChart, BalanceHistoryPlot, PoolHistoryPlot, hex_to_rgba

################################################################################################
# POOL HOME (view)
################################################################################################
def pool_home(request):
    pools = Pool.objects.all()
        
    return render(request, 'pool/pool_home.html', {
        'pools': pools,
        'data_current_balances': json.dumps(CurrentBalancesBarChart(pools)),
        'data_reserve_pools': json.dumps(PoolHistoryPlot(pools.filter(type='reserve'))),
        'data_cost_pools': json.dumps(PoolHistoryPlot(pools.filter(type='cost'))),
        'data_investment_pools': json.dumps(PoolHistoryPlot(pools.filter(type='investment'))),
    })


################################################################################################
# INDIVIDUAL POOL (view)
################################################################################################
def pool_detail(request, pool_id):
    pool = get_object_or_404(Pool, id=pool_id)
    
    if request.method == 'POST':
        form = PoolForm(request.POST, instance=pool)
        if form.is_valid():
            form.save()
    else:
        form = PoolForm(instance=pool)

    # Prepare chart data with balance history and diluted colors
    chart_data = BalanceHistoryPlot(BalanceHistory.objects.filter(pool=pool))
    color = pool.color
    diluted_color = hex_to_rgba(pool.color)
    chart_data['colors'] = color
    chart_data['diluted_colors'] = diluted_color
    
    return render(request, 'pool/pool_detail.html', {
        'pool': pool,
        'form': form,
        'chart_data': json.dumps(chart_data),
    })

################################################################################################
# POOL TRANSFER (view)
################################################################################################
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


################################################################################################
# POOL UPDATE (view)
################################################################################################
def pool_update(request, pool_id):
    pool = get_object_or_404(Pool, id=pool_id)
    if request.method == 'POST':
        form = PoolForm(request.POST, instance=pool)
        if form.is_valid():
            form.save()
            # Redirect to the pools home page after updating values in the database
            return redirect('pool_home')  # Corrected URL name
    else:
        form = PoolForm()
    return render(request, 'pool/pool_detail.html', {'form': form, 'pool': pool})