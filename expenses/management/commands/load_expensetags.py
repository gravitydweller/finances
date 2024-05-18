# management/commands/load_expensetags.py

import os
import json
from django.core.management.base import BaseCommand
from expenses.models import ExpenseTag  # Corrected import statement
from pools.models import Pool

class Command(BaseCommand):
    help = 'Load expense tags data from JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('expenses', 'fixtures', 'load_expensetags.json')

        with open(file_path) as f:
            expensetags_data = json.load(f)

        for expensetag_data in expensetags_data:
            fields = expensetag_data['fields']
            source_pool_name = fields['source_pool']
            source_pool = Pool.objects.get(name=source_pool_name)
            ExpenseTag.objects.create(  # Updated model name
                name=fields['name'],
                source_pool=source_pool
            )
        
        self.stdout.write(self.style.SUCCESS('Expense tags data loaded successfully'))