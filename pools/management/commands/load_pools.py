# management/commands/load_pools.py

import os
import json
from django.core.management.base import BaseCommand
from pools.models import Pool

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Get the absolute path to the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the pools.json file
        file_path = os.path.join(current_dir, '..', '..', 'fixtures', 'load_pools.json')

        with open(file_path) as f:
            pools_data = json.load(f)

        for pool_data in pools_data:
            fields = pool_data['fields']
            Pool.objects.update_or_create(
                pk=pool_data['pk'],
                defaults={
                    'name': fields['name'],
                    'type': fields['type'],
                    'current_balance': fields['current_balance'],
                    'allocated_procentage': fields['allocated_procentage'],
                    'allocated_fixed': fields['allocated_fixed'],
                    'color': fields['color']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Pools data loaded successfully'))