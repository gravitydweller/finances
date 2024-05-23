# incomes/management/commands/fake_income.py

import random
from datetime import date
from django.core.management.base import BaseCommand
from incomes.models import Income, Employer


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
                
                self.stdout.write(self.style.SUCCESS(f'Fake income created: {income}'))
            else:
                self.stdout.write(self.style.WARNING(f'An income with the same date already exists for {employer}'))
