# incomes/management/commands/fake_income.py

import random
from datetime import date
from django.core.management.base import BaseCommand
from incomes.models import Income, Employer
from allocations.models import allocate_income_to_pools  # Import the function

# incomes/management/commands/fake_income.py

import random
from datetime import date
from django.core.management.base import BaseCommand
from incomes.models import Income, Employer

'''
class Command(BaseCommand):
    help = 'Generate fake income data'

    def handle(self, *args, **options):
        employers = Employer.objects.all()
        tag_choices = ['salary'] * 9 + ['other']  # 90% chance of 'salary' tag
        
        for i in range(100):  # Generate 100 fake income records
            employer = random.choice(employers)
            tag = random.choice(tag_choices)
            amount = round(random.uniform(1980, 2480), 2)  # Random amount between 1980 and 2680
            year = random.randint(2022, date.today().year)
            month = random.randint(1, 12)
            day = 15  # Fixed day as 15th of the month
            date_generated = date(year, month, day)
            
            # Check if an income with the same date already exists
            existing_income = Income.objects.filter(employer=employer, date=date_generated).exists()
            if not existing_income:
                # Create the income instance
                income = Income.objects.create(
                    employer=employer,
                    tag=tag,
                    amount=amount,
                    date=date_generated,
                    allocated=False
                )
                
                # Allocate the income to pools
                allocate_income_to_pools(income)

                self.stdout.write(self.style.SUCCESS(f'Fake income created: {income}'))
            else:
                self.stdout.write(self.style.WARNING(f'An income with the same date already exists for {employer}'))

'''
################################################################################################################################################


# incomes/management/commands/fake_income.py

import random
from datetime import date
from django.core.management.base import BaseCommand
from django.db.models import Count
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
        tag_choices = ['salary'] * 9 + ['other']  # 90% chance of 'salary' tag
        
        for i in range(100):  # Generate 100 fake income records
            employer = random.choice(employers)
            tag = random.choice(tag_choices)
            amount = round(random.uniform(1980, 2180), 2)  # Random amount between 1980 and 2180
            year = random.randint(2022, date.today().year)
            month = random.randint(1, 12)
            day = 15  # Fixed day as 15th of the month
            date_generated = date(year, month, day)
            
            # Check if there is already one income entry for the same month
            existing_incomes = Income.objects.filter(
                employer=employer,
                date__year=year,
                date__month=month
            ).count()
            
            if existing_incomes >= 1:
                self.stdout.write(self.style.WARNING(f'An income entry already exists for {employer} in {year}-{month}. Skipping...'))
                continue
            
            # Check if an income with the same date already exists
            existing_income = Income.objects.filter(employer=employer, date=date_generated).exists()
            if not existing_income:
                # Create the income instance
                income = Income.objects.create(
                    employer=employer,
                    tag=tag,
                    amount=amount,
                    date=date_generated,
                    allocated=False
                )
                
                # Allocate income to pools
                self.allocate_income_to_pools(income)
                
                self.stdout.write(self.style.SUCCESS(f'Fake income created: {income}'))
            else:
                self.stdout.write(self.style.WARNING(f'An income with the same date already exists for {employer}'))
