# expenses/management/commands/fake_expenses.py

import random
from datetime import date
from django.core.management.base import BaseCommand
from expenses.models import Expense, ExpenseChategory, ExpenseTag
from pools.models import Pool

class Command(BaseCommand):
    help = 'Generate fake expense data'

    def handle(self, *args, **options):
        categories = ExpenseChategory.objects.all()
        pools = Pool.objects.all()

        # Define tags and associate them with random pools
        tag_pool_mapping = {
            'food': random.choice(pools),
            'transport': random.choice(pools),
            'utilities': random.choice(pools),
            'entertainment': random.choice(pools),
            'other': random.choice(pools)
        }
        
        # Create or retrieve the ExpenseTags
        tag_instances = {
            tag: ExpenseTag.objects.get_or_create(name=tag, source_pool=pool)[0]
            for tag, pool in tag_pool_mapping.items()
        }

        for i in range(100):  # Generate 100 fake expense records
            category = random.choice(categories)
            tag = random.choice(list(tag_instances.values()))
            amount = round(random.uniform(10, 500), 2)  # Random amount between 10 and 500
            year = random.randint(2022, date.today().year)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # Random day in the month
            date_generated = date(year, month, day)
            description = f'Fake expense for {tag.name}'

            # Create the expense instance
            expense = Expense.objects.create(
                tag=tag,
                chategory=category,
                amount=amount,
                date=date_generated,
                description=description
            )

            self.stdout.write(self.style.SUCCESS(f'Fake expense created: {expense}'))

