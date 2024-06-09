# pools/utils.py

from .models import Pool, BalanceHistory
from django.db.models import DecimalField
from django.db.models.functions import Cast
from datetime import datetime, timedelta
from django.urls import reverse

def hex_to_rgba(hex_color, alpha=0.08):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'


################################################################################################
# CurrentBalancesBarChart  (function)
################################################################################################

def CurrentBalancesBarChart(queryset):
    chart_data = {
        'pool_names': [],
        'current_balances': [],
        'colors': [],
        'diluted_colors': [],
        'urls': []  # Adding a list to hold URLs
    }
    for pool in queryset:
        chart_data['pool_names'].append(pool.name)
        chart_data['current_balances'].append(float(pool.current_balance))
        chart_data['colors'].append(pool.color)
        chart_data['diluted_colors'].append(hex_to_rgba(pool.color, 0.2))  # More transparent color
        chart_data['urls'].append(reverse('pool_detail', args=[pool.id]))
    
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

def PoolHistoryPlot(queryset, time_period='last_year'):

    # Determine the start date based on the time period
    if time_period == 'last_year':
        start_date = datetime.now() - timedelta(days=365)
    elif time_period == 'last_6_months':
        start_date = datetime.now() - timedelta(days=30 * 6)
    elif time_period == 'last_3_months':
        start_date = datetime.now() - timedelta(days=30 * 3)

    # Initialize a dictionary to store histories for each pool
    pools_histories = {pool.name: {'balances': [], 'color': pool.color, 'diluted_color': hex_to_rgba(pool.color)} for pool in queryset}
    # Initialize a set to store unique dates
    dates_set = set()

    # Fetch all BalanceHistory records for the specified pools
    #balance_histories = BalanceHistory.objects.filter(pool__in=queryset).order_by('date')

    # Filter balance history records based on start date
    balance_histories = BalanceHistory.objects.filter(
        pool__in=queryset,
        date__gte=start_date
    ).order_by('date')

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
            'color': data['color'],
            'diluted_color': data['diluted_color'],  # Include diluted color
        }

    return chart_data

