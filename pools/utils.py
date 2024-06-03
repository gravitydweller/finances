# pools/utils.py

from .models import Pool, BalanceHistory
from django.db.models import DecimalField
from django.db.models.functions import Cast


################################################################################################
# CurrentBalancesBarChart  (function)
################################################################################################
'''
def CurrentBalancesBarChart(queryset):
    # Extract pool names, current balances, and colors
    pool_names = [pool.name for pool in queryset]
    current_balances = [float(pool.current_balance) for pool in queryset]
    colors = [pool.color for pool in queryset]
    
    # Prepare chart data
    chart_data = {
        'pool_names': pool_names,
        'current_balances': current_balances,
        'colors': colors,
    }

    return chart_data

'''
def CurrentBalancesBarChart(queryset):
    chart_data = {
        'pool_names': [],
        'current_balances': [],
        'colors': []
    }
    for pool in queryset:
        chart_data['pool_names'].append(pool.name)
        chart_data['current_balances'].append(float(pool.current_balance))
        chart_data['colors'].append(pool.color)
    return chart_data



################################################################################################
# BalanceHistoryPlot  (function)
################################################################################################
def BalanceHistoryPlot(queryset):
    # Filter the balance history records from the queryset and order by date
    balance_history = queryset.order_by('date')
    
    # Convert Decimal objects to float for balance field
    balance_history = balance_history.annotate(balance_float=Cast('balance', DecimalField(max_digits=10, decimal_places=2)))
    
    # Extract dates and balances from the queryset
    dates = [entry.date.strftime('%Y-%m-%d') for entry in balance_history]
    balances = [float(entry.balance_float) for entry in balance_history]

    # Prepare the balance history data
    BalanceHistoryData = {
        'dates': dates,
        'balances': balances,
    }

    return BalanceHistoryData

################################################################################################
# PoolHistoryPlot (function)
################################################################################################
'''
def PoolHistoryPlot(queryset):
    # Initialize a dictionary to store histories for each pool
    pools_histories = {pool.name: [] for pool in queryset}
    # Initialize a set to store unique dates
    dates_set = set()

    # Fetch all BalanceHistory records for the specified pools
    balance_histories = BalanceHistory.objects.filter(pool__in=queryset).order_by('date')
    # Convert Decimal objects to float for balance field
    balance_histories = balance_histories.annotate(balance_float=Cast('balance', DecimalField(max_digits=10, decimal_places=2)))

    # Populate pools_histories with dates and balances
    for entry in balance_histories:
        dates_set.add(entry.date)
        pools_histories[entry.pool.name].append((entry.date.strftime('%Y-%m-%d %H:%M:%S'), float(entry.balance_float)))  # Include time in date format

    # Sort dates
    sorted_dates = sorted(dates_set)

    # Prepare chart data with sorted dates and balances for each pool
    chart_data = {
        'dates': [date.strftime('%Y-%m-%d %H:%M:%S') for date in sorted_dates],  # Include time in date format
        'balances': {}
    }

    for pool_name in pools_histories:
        pool_balances = []
        balance_history_dict = {date: balance for date, balance in pools_histories[pool_name]}
        last_balance = 0.0
        for date in sorted_dates:
            date_str = date.strftime('%Y-%m-%d %H:%M:%S')  # Include time in date format
            if date_str in balance_history_dict:
                last_balance = balance_history_dict[date_str]
            pool_balances.append(last_balance)
        chart_data['balances'][pool_name] = pool_balances

    return chart_data

'''
def PoolHistoryPlot(queryset):
    # Initialize a dictionary to store histories for each pool
    pools_histories = {pool.name: {'balances': [], 'color': pool.color} for pool in queryset}
    # Initialize a set to store unique dates
    dates_set = set()

    # Fetch all BalanceHistory records for the specified pools
    balance_histories = BalanceHistory.objects.filter(pool__in=queryset).order_by('date')
    # Convert Decimal objects to float for balance field
    balance_histories = balance_histories.annotate(balance_float=Cast('balance', DecimalField(max_digits=10, decimal_places=2)))

    # Populate pools_histories with dates and balances
    for entry in balance_histories:
        dates_set.add(entry.date)
        pools_histories[entry.pool.name]['balances'].append((entry.date.strftime('%Y-%m-%d %H:%M:%S'), float(entry.balance_float)))  # Include time in date format

    # Sort dates
    sorted_dates = sorted(dates_set)

    # Prepare chart data with sorted dates and balances for each pool
    chart_data = {
        'dates': [date.strftime('%Y-%m-%d %H:%M:%S') for date in sorted_dates],  # Include time in date format
        'pools': {}
    }

    for pool_name, data in pools_histories.items():
        pool_balances = []
        balance_history_dict = {date: balance for date, balance in data['balances']}
        last_balance = 0.0
        for date in sorted_dates:
            date_str = date.strftime('%Y-%m-%d %H:%M:%S')  # Include time in date format
            if date_str in balance_history_dict:
                last_balance = balance_history_dict[date_str]
            pool_balances.append(last_balance)
        chart_data['pools'][pool_name] = {
            'balances': pool_balances,
            'color': data['color']
        }

    return chart_data
