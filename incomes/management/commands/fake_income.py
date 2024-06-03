# incomes/management/commands/fake_income.py

import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from incomes.models import Income, Employer
from pools.models import Pool, BalanceHistory

class Command(BaseCommand):
    help = 'Generate fake income data'

    def allocate_income_to_pools(self, income_instance):
        income_amount = float(income_instance.amount)
        pools = Pool.objects.all()

        # Calculate total fixed amount for all pools
        total_fixed_amount = sum(pool.allocated_fixed for pool in pools)

        # Ensure allocation_amount_fixed is a float
        allocation_amount_fixed = min(total_fixed_amount, income_amount)

        # Calculate allocation amount for proportional distribution
        allocation_amount_proportion = income_amount - allocation_amount_fixed

        # Distribute remaining amount proportionally to pools based on their percentages
        for pool in pools:
            pool_allocation_proportion = (pool.allocated_procentage / 100) * allocation_amount_proportion
            pool_allocation_total = pool_allocation_proportion + pool.allocated_fixed
            pool.current_balance += pool_allocation_total
            pool.save()

            # Create balance history with the income date
            BalanceHistory.objects.create(pool=pool, balance=pool.current_balance, date=income_instance.date)

    def handle(self, *args, **options):
        employers = Employer.objects.all()
        tag_choices = ['salary'] 
        
        # Start generating fake income records for the previous year
        start_date = date.today().replace(day=15) - timedelta(days=365)  
        end_date = start_date + timedelta(days=365)  # One year from the start date
        
        # Generate income for each month
        current_date = start_date
        while current_date <= end_date:
            employer = random.choice(employers)
            tag = random.choice(tag_choices)
            amount = round(random.uniform(1980, 2180), 2)  # Random amount between 1980 and 2180
            
            # Create the income instance
            income = Income.objects.create(
                employer=employer,
                tag=tag,
                amount=amount,
                date=current_date,
                allocated=False
            )
            
            # Allocate income to pools
            self.allocate_income_to_pools(income)
            
            self.stdout.write(self.style.SUCCESS(f'Fake income created: {income}'))
            
            # Move to the next month
            current_date = current_date.replace(day=15)  # Set the day to the 15th of the next month
            current_date += timedelta(days=30)  # Assuming 30 days in a month
