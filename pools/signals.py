# pools/signals.py

import json
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from .models import Pool

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if sender.name == 'pools':
        # Check if the Pool table is empty
        if not Pool.objects.exists():
            # Load the JSON data
            initial_data = [
                {
                    "model": "pools.pool",
                    "pk": 1,
                    "fields": {
                        "name": "hard times",
                        "type": "reserve",
                        "current_balance": 0.00,
                        "allocated_procentage": 6.00,
                        "allocated_fixed": 85.00,
                        "color": "#856BE8"
                    }
                },
                {
                    "model": "pools.pool",
                    "pk": 2,
                    "fields": {
                        "name": "good times",
                        "type": "reserve",
                        "current_balance": 0.00,
                        "allocated_procentage": 4.00,
                        "allocated_fixed": 35.00,
                        "color": "#AE6BE8"
                    }
                },
                {
                    "model": "pools.pool",
                    "pk": 3,
                    "fields": {
                        "name": "rigid expenses",
                        "type": "cost",
                        "current_balance": 0.00,
                        "allocated_procentage": 40.00,
                        "allocated_fixed": 0.00,
                        "color": "#B8BEE8"
                    }
                },
                {
                    "model": "pools.pool",
                    "pk": 4,
                    "fields": {
                        "name": "basic expenses",
                        "type": "cost",
                        "current_balance": 0.00,
                        "allocated_procentage": 50.00,
                        "allocated_fixed": 0.00,
                        "color": "#6BC9E8"
                    }
                },
                {
                    "model": "pools.pool",
                    "pk": 5,
                    "fields": {
                        "name": "soft expenses",
                        "type": "cost",
                        "current_balance": 0.00,
                        "allocated_procentage": 0.00,
                        "allocated_fixed": 40.00,
                        "color": "#6B79E8"
                    }
                },
                {
                    "model": "pools.pool",
                    "pk": 6,
                    "fields": {
                        "name": "volt",
                        "type": "investment",
                        "current_balance": 0.00,
                        "allocated_procentage": 0.00,
                        "allocated_fixed": 45.00,
                        "color": "#6BA1E8"
                    }
                }
            ]
            for entry in initial_data:
                Pool.objects.create(
                    id=entry['pk'],
                    name=entry['fields']['name'],
                    type=entry['fields']['type'],
                    current_balance=entry['fields']['current_balance'],
                    allocated_procentage=entry['fields']['allocated_procentage'],
                    allocated_fixed=entry['fields']['allocated_fixed'],
                    color=entry['fields']['color']
                )
