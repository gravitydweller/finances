# expenses/management/commands/fake_expenses.py

import random
import os
import json
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from expenses.models import Expense, ExpenseCategory, ExpenseTag

import os
import json
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from expenses.models import Expense, ExpenseCategory, ExpenseTag

class Command(BaseCommand):
    help = 'Generate fake expense data'

    def load_distribution_data(self):
        file_path = "/Users/tilenstruc/HOME/code/finances/expenses/fixtures/expense_destribution_data.json"
        with open(file_path) as f:
            return json.load(f)

    def handle(self, *args, **options):
        categories = ExpenseCategory.objects.all()
        tag_distribution_data = self.load_distribution_data()

        # Define tags and their distribution settings
        tag_settings = {
            data['tag']: {
                'weekly_frequency': data['weekly_frequency'],
                'amount_min': data['amount_min'],
                'amount_max': data['amount_max']
            }
            for data in tag_distribution_data
        }

        # Generate expenses for one year from the current date
        start_date = date.today() - timedelta(days=365)
        end_date = date.today()

        current_date = start_date
        while current_date <= end_date:
            for tag_name, settings in tag_settings.items():
                tags = ExpenseTag.objects.filter(name=tag_name)
                if not tags.exists():
                    continue  # Skip if no tags are found

                weekly_frequency = settings['weekly_frequency']
                amount_min = settings['amount_min']
                amount_max = settings['amount_max']

                # Determine if an expense should be created for this day
                if random.random() < (weekly_frequency / 7):
                    tag = random.choice(tags)  # Randomly select one of the tags if multiple
                    category = random.choice(categories)
                    amount = round(random.uniform(amount_min, amount_max), 2)
                    description = f'Fake expense for {tag.name}'

                    # Create the expense instance
                    expense = Expense.objects.create(
                        tag=tag,
                        category=category,
                        amount=amount,
                        date=current_date,
                        description=description
                    )

                    self.stdout.write(self.style.SUCCESS(f'Fake expense created: {expense}'))

            # Move to the next day
            current_date += timedelta(days=1)
