# incomes/management/commands/fake_employer.py

import random
from django.core.management.base import BaseCommand
from incomes.models import Employer

class Command(BaseCommand):
    help = 'Generate fake employer data'

    def handle(self, *args, **options):
        employer_names = [
            'Lotrič', 'Stark Insudtries', 'Massive Dynamics', 'Google', 'NASA'
        ]

        for name in employer_names:
            # Check if an employer with the same name already exists
            existing_employer = Employer.objects.filter(name=name).exists()
            if not existing_employer:
                # Create the employer instance
                employer = Employer.objects.create(name=name)
                
                self.stdout.write(self.style.SUCCESS(f'Fake employer created: {employer}'))
            else:
                self.stdout.write(self.style.WARNING(f'An employer with the name {name} already exists'))
