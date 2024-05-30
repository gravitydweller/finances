# core/management/commands/cleardata.py

from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Clears all data from the database without deleting the tables.'

    def handle(self, *args, **kwargs):
        for model in apps.get_models():
            model.objects.all().delete()
            self.stdout.write(f'All data from {model._meta.db_table} deleted.')
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from the database.'))

