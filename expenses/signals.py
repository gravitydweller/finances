# expenses/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import ExpenseTag, ExpenseCategory
from pools.models import Pool

@receiver(post_migrate)
def load_initial_expense_data(sender, **kwargs):
    if sender.name == 'expenses':
        # Check if the ExpenseCategory table is empty
        if not ExpenseCategory.objects.exists():
            # Load the initial data for ExpenseCategory
            initial_categories = [
                {"name": "normal expense"},
                {"name": "gas expense"},
                {"name": "utility expense"},
                {"name": "car expense"},
                {"name": "emergency expense"},
                {"name": "loan expense"},
            ]
            for category in initial_categories:
                ExpenseCategory.objects.create(name=category['name'])

        # Check if the ExpenseTag table is empty
        if not ExpenseTag.objects.exists():
            # Load the initial data for ExpenseTag
            initial_tags = [
                {"name": "groceries", "source_pool": "basic expenses", "color": "#59CDDE"},
                {"name": "self-care", "source_pool": "basic expenses", "color": "#DE5FD0"},
                {"name": "home-care", "source_pool": "basic expenses", "color": "#FF756E"},
                {"name": "home maintenance", "source_pool": "basic expenses", "color": "#28007D"},
                {"name": "NLB", "source_pool": "rigid expenses", "color": "#28007D"},
                {"name": "UniCredit Bank", "source_pool": "rigid expenses", "color": "#DF5547"},
                {"name": "weed", "source_pool": "basic expenses", "color": "#DE6764"},
                {"name": "online expense", "source_pool": "soft expenses", "color": "#A3DED2"},
                {"name": "gas", "source_pool": "basic expenses", "color": "#FFF170"},
                {"name": "outside dining", "source_pool": "basic expenses", "color": "#C150DE"},
                {"name": "emergency cost", "source_pool": "hard times", "color": "#59DE96"},
                {"name": "utility", "source_pool": "basic expenses", "color": "#DE6250"}
            ]
            for tag in initial_tags:
                source_pool = Pool.objects.get(name=tag['source_pool'])
                ExpenseTag.objects.create(
                    name=tag['name'],
                    source_pool=source_pool,
                    color=tag['color']
                )
