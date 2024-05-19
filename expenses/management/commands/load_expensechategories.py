# management/commands/load_expensechategories.py

import os
import json
from django.core.management.base import BaseCommand
from expenses.models import ExpenseChategory

class Command(BaseCommand):
    help = 'Load expense categories data from JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('expenses', 'fixtures', 'load_expensechategories.json')

        with open(file_path) as f:
            expensechategories_data = json.load(f)

        for expensechategory_data in expensechategories_data:
            fields = expensechategory_data['fields']
            ExpenseChategory.objects.create(
                name=fields['name']
            )

        self.stdout.write(self.style.SUCCESS('Expense categories data loaded successfully'))