# management/commands/load_expensecategories.py

import os
import json
from django.core.management.base import BaseCommand
from expenses.models import ExpenseCategory

class Command(BaseCommand):
    help = 'Load expense categories data from JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('expenses', 'fixtures', 'load_expensecategories.json')

        with open(file_path) as f:
            expensecategories_data = json.load(f)

        for expensecategory_data in expensecategories_data:
            fields = expensecategory_data['fields']
            ExpenseCategory.objects.create(
                name=fields['name']
            )

        self.stdout.write(self.style.SUCCESS('Expense categories data loaded successfully'))